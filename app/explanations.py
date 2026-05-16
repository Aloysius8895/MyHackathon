from app.models import NormalizedProfile, ScoreBreakdown


class GroundedExplanationService:
    """Builds explanations only from profile fields and score evidence."""

    def explain(self, company: NormalizedProfile, mentor: NormalizedProfile, score: ScoreBreakdown, evidence: list[str]) -> tuple[str, str | None]:
        strongest = sorted(
            [
                ("industry", score.industry_match),
                ("needs/expertise", score.needs_expertise_match),
                ("stage/context", score.stage_context_match),
                ("semantic similarity", score.semantic_similarity),
                ("availability/capacity", score.availability_capacity),
                ("historical feedback", score.historical_feedback),
                ("programme/geography", score.programme_geography_fit),
            ],
            key=lambda item: item[1],
            reverse=True,
        )[:3]
        reasons = ", ".join(f"{name} {value:.0%}" for name, value in strongest)
        reason = (
            f"{mentor.display_name} is recommended for {company.display_name} because the strongest grounded signals are "
            f"{reasons}. Evidence: {'; '.join(evidence[:3]) or 'eligible candidate with available capacity'}."
        )
        risk_note = None
        if score.availability_capacity < 0.5:
            risk_note = "Capacity is limited, so admin should confirm mentor availability before approval."
        if score.needs_expertise_match < 0.4:
            risk_note = "Needs/expertise fit is moderate, so admin should review the profile evidence carefully."
        return reason, risk_note
