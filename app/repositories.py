import asyncio
import hashlib
import re
from typing import Any, Protocol
from uuid import uuid4

from app.models import (
    ExtractedProfileDocument,
    ExtractionActorType,
    ExtractionLog,
    FeedbackEntry,
    FeedbackRequest,
    NormalizedProfile,
    ProfileType,
    Recommendation,
    RecommendationStatus,
    Relationship,
    RelationshipStatus,
    utc_now,
)
from app.scoring import bayesian_average, text_embedding


def _history_text(value: Any) -> str:
    return str(value or "").strip()


def _first_history_value(source: dict[str, Any], keys: list[str], fallback: str = "") -> str:
    for key in keys:
        value = _history_text(source.get(key))
        if value:
            return value
    return fallback


def _history_doc_id(prefix: str, *values: Any) -> str:
    basis = " ".join(_history_text(value) for value in values if _history_text(value)) or prefix
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]
    slug = re.sub(r"[^a-z0-9]+", "_", basis.lower()).strip("_")[:48] or "item"
    return f"{prefix}_{slug}_{digest}"


def _history_response(
    companies: list[dict[str, Any]],
    mentors: list[dict[str, Any]],
    engagements: list[dict[str, Any]],
    latest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base = latest.copy() if latest else {}
    base["companies"] = sorted(companies, key=lambda item: _history_text(item.get("name")).casefold())
    base["mentors"] = sorted(mentors, key=lambda item: _history_text(item.get("name")).casefold())
    base["engagements"] = sorted(
        engagements,
        key=lambda item: (_history_text(item.get("date")), _history_text(item.get("session_id"))),
        reverse=True,
    )
    return base


def _normalize_history_upload(data: dict[str, Any]) -> dict[str, Any]:
    uploaded_at = _history_text(data.get("uploadedAt")) or utc_now().isoformat()
    normalized: dict[str, Any] = {
        **data,
        "uploadedAt": uploaded_at,
        "companies": [],
        "mentors": [],
        "engagements": [],
    }
    mentor_by_id: dict[str, dict[str, Any]] = {}
    mentor_by_name: dict[str, dict[str, Any]] = {}

    for index, mentor in enumerate(data.get("mentors") or []):
        item = dict(mentor)
        name = _first_history_value(item, ["name", "mentor_name", "mentorName", "lecturer", "lecturerName"])
        source_id = _first_history_value(item, ["id", "source_id", "sourceId"], f"mentor_{index + 1}")
        history_id = _history_doc_id("mentor", name, source_id)
        item.update(
            {
                "id": source_id,
                "history_id": history_id,
                "name": name or source_id,
                "nameKey": (name or source_id).casefold(),
                "updatedAt": uploaded_at,
            }
        )
        normalized["mentors"].append(item)
        mentor_by_id[source_id.casefold()] = item
        mentor_by_id[history_id.casefold()] = item
        if name:
            mentor_by_name[name.casefold()] = item

    for index, company in enumerate(data.get("companies") or []):
        item = dict(company)
        name = _first_history_value(item, ["name", "company", "company_name", "companyName"])
        source_id = _first_history_value(item, ["id", "source_id", "sourceId"], f"company_{index + 1}")
        item.update(
            {
                "id": source_id,
                "history_id": _history_doc_id("company", name, source_id),
                "name": name or source_id,
                "nameKey": (name or source_id).casefold(),
                "updatedAt": uploaded_at,
            }
        )
        normalized["companies"].append(item)

    for index, engagement in enumerate(data.get("engagements") or []):
        item = dict(engagement)
        mentor_id = _first_history_value(item, ["mentor_id", "mentorId"])
        mentor_name = _first_history_value(item, ["mentor_name", "mentorName", "lecturer", "lecturerName", "mentor"])
        mentor = mentor_by_id.get(mentor_id.casefold()) if mentor_id else None
        if not mentor and mentor_name:
            mentor = mentor_by_name.get(mentor_name.casefold())
        if not mentor_name and mentor:
            mentor_name = _history_text(mentor.get("name"))
        if not mentor_id and mentor:
            mentor_id = _history_text(mentor.get("id")) or _history_text(mentor.get("history_id"))

        session_id = _first_history_value(item, ["session_id", "sessionId", "id"])
        company_name = _first_history_value(item, ["company_name", "companyName", "company", "startup", "startup_name"])
        topic = _first_history_value(item, ["outcome", "topic", "result"])
        history_id = _history_doc_id(
            "session",
            session_id,
            mentor_name,
            company_name,
            topic,
            item.get("date"),
            index,
        )
        item.update(
            {
                "history_id": history_id,
                "session_id": session_id or history_id,
                "mentor_id": mentor_id,
                "mentor_name": mentor_name,
                "mentor_history_id": _history_text(mentor.get("history_id")) if mentor else "",
                "company_name": company_name,
                "updatedAt": uploaded_at,
            }
        )
        normalized["engagements"].append(item)
    return normalized


class Repository(Protocol):
    async def save_profile(self, profile: NormalizedProfile) -> NormalizedProfile: ...
    async def get_profile(self, profile_id: str) -> NormalizedProfile | None: ...
    async def list_profiles(self, profile_type: ProfileType | None = None) -> list[NormalizedProfile]: ...
    async def list_companies(self) -> list[NormalizedProfile]: ...
    async def list_mentors(self) -> list[NormalizedProfile]: ...
    async def save_extracted_actor(self, document: ExtractedProfileDocument, normalized_profile: NormalizedProfile) -> ExtractedProfileDocument: ...
    async def get_extracted_actor(self, actor_type: ExtractionActorType, actor_id: str) -> ExtractedProfileDocument | None: ...
    async def write_extraction_log(self, log: ExtractionLog) -> ExtractionLog: ...
    async def get_latest_extraction_log(self, actor_type: ExtractionActorType, actor_id: str) -> ExtractionLog | None: ...
    async def save_recommendation(self, recommendation: Recommendation) -> Recommendation: ...
    async def get_recommendation(self, recommendation_id: str) -> Recommendation | None: ...
    async def list_recommendations(self, status: RecommendationStatus | None = None) -> list[Recommendation]: ...
    async def save_relationship(self, relationship: Relationship) -> Relationship: ...
    async def get_relationship(self, relationship_id: str) -> Relationship | None: ...
    async def list_relationships(self, status: RelationshipStatus | None = None) -> list[Relationship]: ...
    async def add_feedback(self, relationship_id: str, feedback: FeedbackRequest) -> Relationship: ...
    async def increment_active_assignments(self, mentor_id: str) -> None: ...
    async def save_history_upload(self, data: dict[str, Any]) -> None: ...
    async def get_history_upload(self) -> dict[str, Any] | None: ...


class InMemoryRepository:
    def __init__(self, seed_demo_data: bool = True) -> None:
        self.profiles: dict[str, NormalizedProfile] = {}
        self.extracted_actors: dict[tuple[ExtractionActorType, str], ExtractedProfileDocument] = {}
        self.extraction_logs: dict[str, ExtractionLog] = {}
        self.recommendations: dict[str, Recommendation] = {}
        self.relationships: dict[str, Relationship] = {}
        self.feedback: dict[str, list[FeedbackEntry]] = {}
        self._history_upload: dict[str, Any] | None = None
        self._history_companies: dict[str, dict[str, Any]] = {}
        self._history_mentors: dict[str, dict[str, Any]] = {}
        self._history_engagements: dict[str, dict[str, Any]] = {}
        if seed_demo_data:
            self._seed()

    async def save_profile(self, profile: NormalizedProfile) -> NormalizedProfile:
        profile.updated_at = utc_now()
        self.profiles[profile.profile_id] = profile.model_copy(deep=True)
        return profile

    async def get_profile(self, profile_id: str) -> NormalizedProfile | None:
        profile = self.profiles.get(profile_id)
        return profile.model_copy(deep=True) if profile else None

    async def list_profiles(self, profile_type: ProfileType | None = None) -> list[NormalizedProfile]:
        return [
            profile.model_copy(deep=True)
            for profile in self.profiles.values()
            if profile_type is None or profile.profile_type == profile_type
        ]

    async def list_companies(self) -> list[NormalizedProfile]:
        return await self.list_profiles(ProfileType.company)

    async def list_mentors(self) -> list[NormalizedProfile]:
        return await self.list_profiles(ProfileType.mentor)

    async def save_extracted_actor(self, document: ExtractedProfileDocument, normalized_profile: NormalizedProfile) -> ExtractedProfileDocument:
        self.extracted_actors[(document.actor_type, document.actor_id)] = document.model_copy(deep=True)
        await self.save_profile(normalized_profile)
        return document

    async def get_extracted_actor(self, actor_type: ExtractionActorType, actor_id: str) -> ExtractedProfileDocument | None:
        document = self.extracted_actors.get((actor_type, actor_id))
        return document.model_copy(deep=True) if document else None

    async def write_extraction_log(self, log: ExtractionLog) -> ExtractionLog:
        self.extraction_logs[log.log_id] = log.model_copy(deep=True)
        return log

    async def get_latest_extraction_log(self, actor_type: ExtractionActorType, actor_id: str) -> ExtractionLog | None:
        logs = [
            log for log in self.extraction_logs.values()
            if log.actor_type == actor_type and log.actor_id == actor_id
        ]
        if not logs:
            return None
        latest = max(logs, key=lambda log: log.created_at)
        return latest.model_copy(deep=True)

    async def save_recommendation(self, recommendation: Recommendation) -> Recommendation:
        recommendation.updated_at = utc_now()
        self.recommendations[recommendation.recommendation_id] = recommendation.model_copy(deep=True)
        return recommendation

    async def get_recommendation(self, recommendation_id: str) -> Recommendation | None:
        recommendation = self.recommendations.get(recommendation_id)
        return recommendation.model_copy(deep=True) if recommendation else None

    async def list_recommendations(self, status: RecommendationStatus | None = None) -> list[Recommendation]:
        values = self.recommendations.values()
        if status:
            values = [recommendation for recommendation in values if recommendation.status == status]
        return [recommendation.model_copy(deep=True) for recommendation in values]

    async def save_relationship(self, relationship: Relationship) -> Relationship:
        relationship.updated_at = utc_now()
        self.relationships[relationship.relationship_id] = relationship.model_copy(deep=True)
        return relationship

    async def get_relationship(self, relationship_id: str) -> Relationship | None:
        relationship = self.relationships.get(relationship_id)
        return relationship.model_copy(deep=True) if relationship else None

    async def list_relationships(self, status: RelationshipStatus | None = None) -> list[Relationship]:
        values = self.relationships.values()
        if status:
            values = [relationship for relationship in values if relationship.status == status]
        return [relationship.model_copy(deep=True) for relationship in values]

    async def add_feedback(self, relationship_id: str, feedback: FeedbackRequest) -> Relationship:
        relationship = self.relationships.get(relationship_id)
        if not relationship:
            raise KeyError(relationship_id)
        entry = FeedbackEntry(
            feedback_id=f"fb_{uuid4().hex[:12]}",
            relationship_id=relationship_id,
            source_id=feedback.source_id,
            source_role=feedback.source_role,
            rating=feedback.rating,
            comment=feedback.comment,
            outcome=feedback.outcome,
        )
        entries = self.feedback.setdefault(relationship_id, [])
        entries.append(entry)
        relationship.feedback_score = round(bayesian_average([item.rating for item in entries]), 2)
        if feedback.outcome:
            relationship.outcome = feedback.outcome
            relationship.status = RelationshipStatus.completed
        relationship.updated_at = utc_now()
        self.relationships[relationship_id] = relationship
        return relationship.model_copy(deep=True)

    async def increment_active_assignments(self, mentor_id: str) -> None:
        mentor = self.profiles.get(mentor_id)
        if mentor:
            mentor.active_assignments += 1
            mentor.updated_at = utc_now()

    async def save_history_upload(self, data: dict[str, Any]) -> None:
        normalized = _normalize_history_upload(data)
        self._history_upload = normalized
        for company in normalized["companies"]:
            self._history_companies[_history_text(company.get("history_id"))] = company
        for mentor in normalized["mentors"]:
            self._history_mentors[_history_text(mentor.get("history_id"))] = mentor
        for engagement in normalized["engagements"]:
            self._history_engagements[_history_text(engagement.get("history_id"))] = engagement

    async def get_history_upload(self) -> dict[str, Any] | None:
        if not self._history_upload:
            return None
        return _history_response(
            list(self._history_companies.values()),
            list(self._history_mentors.values()),
            list(self._history_engagements.values()),
            self._history_upload,
        )

    def _seed(self) -> None:
        seed_profiles = [
            NormalizedProfile(
                profile_id="cmp_novaai",
                profile_type=ProfileType.company,
                display_name="NovaAI Finance",
                industry=["FinTech", "SaaS"],
                stage="Seed",
                needs=["Fundraising", "Go-to-market"],
                country="Malaysia",
                verified=True,
                tags=["fintech", "fundraising", "seed", "saas"],
                embedding=text_embedding(["fintech seed fundraising saas payments malaysia"]),
            ),
            NormalizedProfile(
                profile_id="men_alina",
                profile_type=ProfileType.mentor,
                display_name="Alina Tan",
                industry=["FinTech"],
                stage="Seed",
                expertise=["Fundraising", "Venture capital", "Go-to-market"],
                country="Malaysia",
                availability=True,
                capacity=3,
                active_assignments=1,
                past_experience=["Mentored seed-stage fintech founders", "Former VC principal"],
                verified=True,
                tags=["fintech", "fundraising", "seed"],
                embedding=text_embedding(["fintech venture capital seed fundraising go to market malaysia"]),
                metadata={"historical_feedback": 4.7},
            ),
            NormalizedProfile(
                profile_id="men_david",
                profile_type=ProfileType.mentor,
                display_name="David Lim",
                industry=["Manufacturing", "IoT"],
                expertise=["Technical architecture", "Supply chain"],
                country="Singapore",
                availability=True,
                capacity=2,
                active_assignments=0,
                past_experience=["Built industrial IoT systems"],
                verified=True,
                tags=["manufacturing", "iot"],
                embedding=text_embedding(["manufacturing industrial iot technical architecture supply chain"]),
                metadata={"historical_feedback": 4.2},
            ),
            NormalizedProfile(
                profile_id="men_lina",
                profile_type=ProfileType.mentor,
                display_name="Lina Gomez",
                industry=["FinTech"],
                expertise=["Product strategy"],
                country="Malaysia",
                availability=False,
                capacity=2,
                active_assignments=0,
                verified=True,
                tags=["fintech", "product"],
                embedding=text_embedding(["fintech product roadmap user discovery"]),
                metadata={"historical_feedback": 4.8},
            ),
        ]
        for profile in seed_profiles:
            self.profiles[profile.profile_id] = profile


class FirestoreRepository:
    """Firestore-backed repository for Cloud Run deployments."""

    def __init__(self) -> None:
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
        except ImportError as exc:
            raise RuntimeError("Install firebase-admin to use storage_backend=firestore") from exc

        if not firebase_admin._apps:
            firebase_admin.initialize_app(credentials.ApplicationDefault())
        self.client = firestore.client()

    async def save_profile(self, profile: NormalizedProfile) -> NormalizedProfile:
        await asyncio.to_thread(
            self.client.collection("profiles").document(profile.profile_id).set,
            profile.model_dump(mode="json"),
        )
        return profile

    async def get_profile(self, profile_id: str) -> NormalizedProfile | None:
        snapshot = await asyncio.to_thread(self.client.collection("profiles").document(profile_id).get)
        return NormalizedProfile(**snapshot.to_dict()) if snapshot.exists else None

    async def list_profiles(self, profile_type: ProfileType | None = None) -> list[NormalizedProfile]:
        collection = self.client.collection("profiles")
        query = collection.where("profile_type", "==", profile_type.value) if profile_type else collection
        snapshots = await asyncio.to_thread(lambda: list(query.stream()))
        return [NormalizedProfile(**snapshot.to_dict()) for snapshot in snapshots]

    async def list_companies(self) -> list[NormalizedProfile]:
        return await self.list_profiles(ProfileType.company)

    async def list_mentors(self) -> list[NormalizedProfile]:
        return await self.list_profiles(ProfileType.mentor)

    async def save_extracted_actor(self, document: ExtractedProfileDocument, normalized_profile: NormalizedProfile) -> ExtractedProfileDocument:
        collection = self._actor_collection(document.actor_type)
        await asyncio.to_thread(
            self.client.collection(collection).document(document.actor_id).set,
            document.model_dump(mode="json", by_alias=True),
        )
        await self.save_profile(normalized_profile)
        return document

    async def get_extracted_actor(self, actor_type: ExtractionActorType, actor_id: str) -> ExtractedProfileDocument | None:
        collection = self._actor_collection(actor_type)
        snapshot = await asyncio.to_thread(self.client.collection(collection).document(actor_id).get)
        return ExtractedProfileDocument.model_validate(snapshot.to_dict()) if snapshot.exists else None

    async def write_extraction_log(self, log: ExtractionLog) -> ExtractionLog:
        await asyncio.to_thread(
            self.client.collection("extraction_logs").document(log.log_id).set,
            log.model_dump(mode="json", by_alias=True),
        )
        return log

    async def get_latest_extraction_log(self, actor_type: ExtractionActorType, actor_id: str) -> ExtractionLog | None:
        query = (
            self.client.collection("extraction_logs")
            .where("actorType", "==", actor_type.value)
            .where("actorId", "==", actor_id)
            .order_by("createdAt", direction="DESCENDING")
            .limit(1)
        )
        snapshots = await asyncio.to_thread(lambda: list(query.stream()))
        return ExtractionLog.model_validate(snapshots[0].to_dict()) if snapshots else None

    async def save_recommendation(self, recommendation: Recommendation) -> Recommendation:
        await asyncio.to_thread(
            self.client.collection("recommendations").document(recommendation.recommendation_id).set,
            recommendation.model_dump(mode="json"),
        )
        return recommendation

    async def get_recommendation(self, recommendation_id: str) -> Recommendation | None:
        snapshot = await asyncio.to_thread(self.client.collection("recommendations").document(recommendation_id).get)
        return Recommendation(**snapshot.to_dict()) if snapshot.exists else None

    async def list_recommendations(self, status: RecommendationStatus | None = None) -> list[Recommendation]:
        collection = self.client.collection("recommendations")
        query = collection.where("status", "==", status.value) if status else collection
        snapshots = await asyncio.to_thread(lambda: list(query.stream()))
        return [Recommendation(**snapshot.to_dict()) for snapshot in snapshots]

    async def save_relationship(self, relationship: Relationship) -> Relationship:
        await asyncio.to_thread(
            self.client.collection("relationships").document(relationship.relationship_id).set,
            relationship.model_dump(mode="json"),
        )
        return relationship

    async def get_relationship(self, relationship_id: str) -> Relationship | None:
        snapshot = await asyncio.to_thread(self.client.collection("relationships").document(relationship_id).get)
        return Relationship(**snapshot.to_dict()) if snapshot.exists else None

    async def list_relationships(self, status: RelationshipStatus | None = None) -> list[Relationship]:
        collection = self.client.collection("relationships")
        query = collection.where("status", "==", status.value) if status else collection
        snapshots = await asyncio.to_thread(lambda: list(query.stream()))
        return [Relationship(**snapshot.to_dict()) for snapshot in snapshots]

    async def add_feedback(self, relationship_id: str, feedback: FeedbackRequest) -> Relationship:
        relationship = await self.get_relationship(relationship_id)
        if not relationship:
            raise KeyError(relationship_id)
        entry = FeedbackEntry(
            feedback_id=f"fb_{uuid4().hex[:12]}",
            relationship_id=relationship_id,
            source_id=feedback.source_id,
            source_role=feedback.source_role,
            rating=feedback.rating,
            comment=feedback.comment,
            outcome=feedback.outcome,
        )
        feedback_ref = self.client.collection("relationship_feedback").document(entry.feedback_id)
        await asyncio.to_thread(feedback_ref.set, entry.model_dump(mode="json"))
        query = self.client.collection("relationship_feedback").where("relationship_id", "==", relationship_id)
        snapshots = await asyncio.to_thread(lambda: list(query.stream()))
        ratings = [int(snapshot.to_dict()["rating"]) for snapshot in snapshots]
        relationship.feedback_score = round(bayesian_average(ratings), 2)
        if feedback.outcome:
            relationship.outcome = feedback.outcome
            relationship.status = RelationshipStatus.completed
        await self.save_relationship(relationship)
        return relationship

    async def increment_active_assignments(self, mentor_id: str) -> None:
        profile = await self.get_profile(mentor_id)
        if not profile:
            return
        profile.active_assignments += 1
        await self.save_profile(profile)

    async def save_history_upload(self, data: dict[str, Any]) -> None:
        normalized = _normalize_history_upload(data)

        def write_history() -> None:
            batch = self.client.batch()
            batch.set(self.client.collection("history_uploads").document("latest"), normalized)
            for company in normalized["companies"]:
                batch.set(
                    self.client.collection("history_companies").document(_history_text(company.get("history_id"))),
                    company,
                    merge=True,
                )
            for mentor in normalized["mentors"]:
                batch.set(
                    self.client.collection("history_mentors").document(_history_text(mentor.get("history_id"))),
                    mentor,
                    merge=True,
                )
            for engagement in normalized["engagements"]:
                batch.set(
                    self.client.collection("history_sessions").document(_history_text(engagement.get("history_id"))),
                    engagement,
                    merge=True,
                )
            batch.commit()

        await asyncio.to_thread(write_history)

    async def get_history_upload(self) -> dict[str, Any] | None:
        def read_history() -> dict[str, Any] | None:
            latest_snapshot = self.client.collection("history_uploads").document("latest").get()
            latest = latest_snapshot.to_dict() if latest_snapshot.exists else None
            companies = [snapshot.to_dict() for snapshot in self.client.collection("history_companies").stream()]
            mentors = [snapshot.to_dict() for snapshot in self.client.collection("history_mentors").stream()]
            engagements = [snapshot.to_dict() for snapshot in self.client.collection("history_sessions").stream()]
            if not latest and not engagements:
                return None
            if not engagements and latest:
                return latest
            return _history_response(companies, mentors, engagements, latest)

        return await asyncio.to_thread(read_history)

    def _actor_collection(self, actor_type: ExtractionActorType) -> str:
        if actor_type == ExtractionActorType.company:
            return "companies"
        return "mentors"
