from uuid import uuid4

from app.explanations import GroundedExplanationService
from app.models import (
    MatchRunRequest,
    MatchRunResponse,
    NormalizedProfile,
    ProfileType,
    Recommendation,
    RecommendationStatus,
    Relationship,
    ScoreBreakdown,
    utc_now,
)
from app.repositories import Repository
from app.scoring import binary_overlap, overlap_score, semantic_score


class MatchingService:
    def __init__(self, repository: Repository, explanation_service: GroundedExplanationService | None = None) -> None:
        self.repository = repository
        self.explanation_service = explanation_service or GroundedExplanationService()

    async def run_company_to_mentor_match(self, request: MatchRunRequest) -> MatchRunResponse:
        company = await self.repository.get_profile(request.company_id)
        if not company:
            raise ValueError("Company profile not found")
        if company.profile_type != ProfileType.company:
            raise ValueError("Only company-to-mentor matching is supported in the MVP")
        if not company.verified:
            raise ValueError("Company must be verified before matching")

        mentors = await self.repository.list_mentors()
        scored = [
            await self._build_recommendation(company, mentor)
            for mentor in mentors
            if self._is_eligible(company, mentor)
        ]
        scored.sort(key=lambda recommendation: recommendation.match_score, reverse=True)
        selected = scored[: request.limit]
        if request.persist_recommendations:
            selected = [await self.repository.save_recommendation(recommendation) for recommendation in selected]
        return MatchRunResponse(company_id=company.profile_id, recommendations=selected)

    async def create_relationship_from_recommendation(self, recommendation: Recommendation, admin_id: str, mentor_id: str | None = None) -> Relationship:
        target_mentor_id = mentor_id or recommendation.mentor_id
        mentor = await self.repository.get_profile(target_mentor_id)
        company = await self.repository.get_profile(recommendation.company_id)
        if not mentor or not company:
            raise ValueError("Company or mentor profile not found")
        if not self._is_eligible(company, mentor):
            raise ValueError("Selected mentor is not eligible for this company")

        score = self._score(company, mentor)
        evidence = self._build_evidence(company, mentor, score)
        reason, _ = self.explanation_service.explain(company, mentor, score, evidence)
        relationship = Relationship(
            relationship_id=f"rel_{uuid4().hex[:12]}",
            company_id=company.profile_id,
            mentor_id=mentor.profile_id,
            match_score=score.final_score,
            match_reason=reason,
            approved_by_admin=admin_id,
            recommendation_id=recommendation.recommendation_id,
        )
        saved = await self.repository.save_relationship(relationship)
        await self.repository.increment_active_assignments(mentor.profile_id)
        return saved

    async def _build_recommendation(self, company: NormalizedProfile, mentor: NormalizedProfile) -> Recommendation:
        score = self._score(company, mentor)
        evidence = self._build_evidence(company, mentor, score)
        reason, risk_note = self.explanation_service.explain(company, mentor, score, evidence)
        return Recommendation(
            recommendation_id=f"rec_{uuid4().hex[:12]}",
            company_id=company.profile_id,
            mentor_id=mentor.profile_id,
            match_score=score.final_score,
            score_breakdown=score,
            match_reason=reason,
            risk_note=risk_note,
            evidence=evidence,
        )

    def _is_eligible(self, company: NormalizedProfile, mentor: NormalizedProfile) -> bool:
        if mentor.profile_type != ProfileType.mentor:
            return False
        if not mentor.verified:
            return False
        if not mentor.availability:
            return False
        if mentor.capacity <= mentor.active_assignments:
            return False
        if company.profile_id in mentor.conflicts or mentor.profile_id in company.conflicts:
            return False
        return True

    def _score(self, company: NormalizedProfile, mentor: NormalizedProfile) -> ScoreBreakdown:
        industry = binary_overlap(company.industry, mentor.industry)
        needs = overlap_score(company.needs, mentor.expertise)
        stage = binary_overlap([company.stage] if company.stage else [], mentor.past_experience + ([mentor.stage] if mentor.stage else []))
        semantic = semantic_score(
            company.needs + company.industry + company.tags,
            mentor.expertise + mentor.industry + mentor.tags + mentor.past_experience,
            company.embedding,
            mentor.embedding,
        )
        capacity_remaining = max(mentor.capacity - mentor.active_assignments, 0)
        availability = capacity_remaining / mentor.capacity if mentor.capacity else 0.0
        historical = min(float(mentor.metadata.get("historical_feedback", 3.5)) / 5, 1.0)
        geography = 1.0 if company.country and company.country == mentor.country else 0.5
        graph_score = self._graph_lite_score(company, mentor)
        final = (
            20 * industry
            + 25 * needs
            + 15 * stage
            + 15 * semantic
            + 10 * availability
            + 10 * max(historical, graph_score)
            + 5 * geography
        )
        return ScoreBreakdown(
            industry_match=round(industry, 3),
            needs_expertise_match=round(needs, 3),
            stage_context_match=round(stage, 3),
            semantic_similarity=round(semantic, 3),
            availability_capacity=round(availability, 3),
            historical_feedback=round(max(historical, graph_score), 3),
            programme_geography_fit=round(geography, 3),
            graph_relationship_score=round(graph_score, 3),
            final_score=round(final, 2),
        )

    def _graph_lite_score(self, company: NormalizedProfile, mentor: NormalizedProfile) -> float:
        graph_terms = mentor.past_experience + mentor.tags + mentor.expertise
        need_overlap = overlap_score(company.needs, graph_terms)
        industry_overlap = binary_overlap(company.industry, graph_terms)
        return min((need_overlap * 0.7) + (industry_overlap * 0.3), 1.0)

    def _build_evidence(self, company: NormalizedProfile, mentor: NormalizedProfile, score: ScoreBreakdown) -> list[str]:
        evidence: list[str] = []
        if score.industry_match > 0:
            evidence.append(f"Industry overlap: {', '.join(company.industry)} with {', '.join(mentor.industry)}")
        if score.needs_expertise_match > 0:
            evidence.append(f"Company needs {', '.join(company.needs)}; mentor expertise includes {', '.join(mentor.expertise)}")
        if score.programme_geography_fit == 1:
            evidence.append(f"Both profiles are linked to {company.country}")
        if score.availability_capacity > 0:
            evidence.append(f"Mentor has {mentor.capacity - mentor.active_assignments} of {mentor.capacity} capacity slots available")
        if score.graph_relationship_score > 0:
            evidence.append("Graph-lite signal found overlap across mentor experience, tags, or expertise")
        return evidence


def mark_recommendation_decision(
    recommendation: Recommendation,
    status: RecommendationStatus,
    admin_id: str,
    note: str | None = None,
    override_mentor_id: str | None = None,
) -> Recommendation:
    recommendation.status = status
    recommendation.approved_by_admin = admin_id if status in {RecommendationStatus.accepted, RecommendationStatus.overridden} else None
    recommendation.admin_note = note
    recommendation.override_mentor_id = override_mentor_id
    recommendation.updated_at = utc_now()
    return recommendation
