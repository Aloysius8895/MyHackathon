from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_string_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for value in values:
        cleaned = value.strip()
        key = cleaned.casefold()
        if not cleaned or key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)
    return normalized


class ProfileType(str, Enum):
    company = "company"
    mentor = "mentor"
    programme = "programme"
    partner = "partner"
    service_provider = "service_provider"


class RelationshipType(str, Enum):
    company_to_mentor = "company_to_mentor"
    company_to_programme = "company_to_programme"
    partner_to_initiative = "partner_to_initiative"
    service_provider_to_company = "service_provider_to_company"


class RecommendationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    overridden = "overridden"


class RelationshipStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class ExtractionActorType(str, Enum):
    company = "company"
    mentor = "mentor"


class ExtractionStatus(str, Enum):
    completed = "completed"
    needs_review = "needs_review"
    failed_invalid_json = "failed_invalid_json"
    failed_validation = "failed_validation"
    failed_low_confidence = "failed_low_confidence"
    failed_firestore = "failed_firestore"


class AvailabilityStatus(str, Enum):
    available = "available"
    limited = "limited"
    unavailable = "unavailable"
    unknown = "unknown"


class CompanyStage(str, Enum):
    idea = "Idea"
    mvp = "MVP"
    pre_seed = "Pre-seed"
    seed = "Seed"
    series_a = "Series A"
    growth = "Growth"
    unknown = "Unknown"


class CamelModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)


class ProfileExtractionRequest(BaseModel):
    profile_id: str | None = None
    profile_type: ProfileType
    raw_text: str = Field(min_length=10)
    display_name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class NormalizedProfile(BaseModel):
    profile_id: str
    profile_type: ProfileType
    display_name: str
    industry: list[str] = Field(default_factory=list)
    stage: str | None = None
    needs: list[str] = Field(default_factory=list)
    expertise: list[str] = Field(default_factory=list)
    country: str | None = None
    availability: bool = True
    programme_eligibility: list[str] = Field(default_factory=list)
    capacity: int = Field(default=0, ge=0)
    active_assignments: int = Field(default=0, ge=0)
    past_experience: list[str] = Field(default_factory=list)
    verified: bool = False
    conflicts: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    embedding: list[float] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @field_validator("industry", "needs", "expertise", "programme_eligibility", "past_experience", "conflicts", "tags")
    @classmethod
    def normalize_terms(cls, values: list[str]) -> list[str]:
        return normalize_string_list(values)


class ScoreBreakdown(BaseModel):
    industry_match: float = Field(ge=0, le=1)
    needs_expertise_match: float = Field(ge=0, le=1)
    stage_context_match: float = Field(ge=0, le=1)
    semantic_similarity: float = Field(ge=0, le=1)
    availability_capacity: float = Field(ge=0, le=1)
    historical_feedback: float = Field(ge=0, le=1)
    programme_geography_fit: float = Field(ge=0, le=1)
    graph_relationship_score: float = Field(ge=0, le=1)
    final_score: float = Field(ge=0, le=100)


class MatchRunRequest(BaseModel):
    company_id: str
    limit: int = Field(default=5, ge=1, le=50)
    persist_recommendations: bool = True


class Recommendation(BaseModel):
    recommendation_id: str
    relationship_type: RelationshipType = RelationshipType.company_to_mentor
    company_id: str
    mentor_id: str
    match_score: float = Field(ge=0, le=100)
    score_breakdown: ScoreBreakdown
    match_reason: str
    risk_note: str | None = None
    evidence: list[str] = Field(default_factory=list)
    status: RecommendationStatus = RecommendationStatus.pending
    approved_by_admin: str | None = None
    override_mentor_id: str | None = None
    admin_note: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class MatchRunResponse(BaseModel):
    company_id: str
    recommendations: list[Recommendation]


class RecommendationDecisionRequest(BaseModel):
    admin_id: str
    note: str | None = None
    override_mentor_id: str | None = None


class Relationship(BaseModel):
    relationship_id: str
    relationship_type: RelationshipType = RelationshipType.company_to_mentor
    company_id: str
    mentor_id: str
    programme_id: str | None = None
    match_score: float = Field(ge=0, le=100)
    match_reason: str
    status: RelationshipStatus = RelationshipStatus.active
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    approved_by_admin: str
    feedback_score: float | None = Field(default=None, ge=0, le=5)
    outcome: str | None = None
    recommendation_id: str | None = None


class FeedbackRequest(BaseModel):
    source_id: str
    source_role: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
    outcome: str | None = None


class FeedbackEntry(BaseModel):
    feedback_id: str
    relationship_id: str
    source_id: str
    source_role: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
    outcome: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


class AuthContext(BaseModel):
    user_id: str
    role: str = "admin"
    claims: dict[str, Any] = Field(default_factory=dict)


class CompanyProfileExtract(CamelModel):
    company_name: str | None = Field(default=None, alias="companyName")
    industry: list[str] = Field(default_factory=list)
    stage: CompanyStage | str | None = "Unknown"
    needs: list[str] = Field(default_factory=list)
    country: str | None = None
    target_market: list[str] = Field(default_factory=list, alias="targetMarket")
    business_model: list[str] = Field(default_factory=list, alias="businessModel")
    preferred_support_types: list[str] = Field(default_factory=list, alias="preferredSupportTypes")
    programme_interest: list[str] = Field(default_factory=list, alias="programmeInterest")
    confidence_score: float = Field(default=0, ge=0, le=1, alias="confidenceScore")
    missing_fields: list[str] = Field(default_factory=list, alias="missingFields")
    extraction_notes: str | None = Field(default=None, alias="extractionNotes")

    @field_validator("industry", "needs", "target_market", "business_model", "preferred_support_types", "programme_interest", "missing_fields")
    @classmethod
    def normalize_lists(cls, values: list[str]) -> list[str]:
        return normalize_string_list(values)


class MentorProfileExtract(CamelModel):
    mentor_name: str | None = Field(default=None, alias="mentorName")
    industries: list[str] = Field(default_factory=list)
    expertise: list[str] = Field(default_factory=list)
    stage_experience: list[str] = Field(default_factory=list, alias="stageExperience")
    country: str | None = None
    availability: AvailabilityStatus | str = AvailabilityStatus.unknown
    max_capacity: int | None = Field(default=None, ge=0, alias="maxCapacity")
    current_capacity: int = Field(default=0, ge=0, alias="currentCapacity")
    past_experience: list[str] = Field(default_factory=list, alias="pastExperience")
    preferred_company_types: list[str] = Field(default_factory=list, alias="preferredCompanyTypes")
    confidence_score: float = Field(default=0, ge=0, le=1, alias="confidenceScore")
    missing_fields: list[str] = Field(default_factory=list, alias="missingFields")
    extraction_notes: str | None = Field(default=None, alias="extractionNotes")

    @field_validator("industries", "expertise", "stage_experience", "past_experience", "preferred_company_types", "missing_fields")
    @classmethod
    def normalize_lists(cls, values: list[str]) -> list[str]:
        return normalize_string_list(values)


class CompanyExtractionRequest(CamelModel):
    company_id: str = Field(alias="companyId", min_length=3, max_length=120, pattern=r"^[A-Za-z0-9_-]+$")
    raw_profile_text: str = Field(alias="rawProfileText", min_length=20, max_length=12000)
    display_name: str | None = Field(default=None, alias="displayName", max_length=200)
    force_reextract: bool = Field(default=False, alias="forceReextract")


class MentorExtractionRequest(CamelModel):
    mentor_id: str = Field(alias="mentorId", min_length=3, max_length=120, pattern=r"^[A-Za-z0-9_-]+$")
    raw_profile_text: str = Field(alias="rawProfileText", min_length=20, max_length=12000)
    display_name: str | None = Field(default=None, alias="displayName", max_length=200)
    force_reextract: bool = Field(default=False, alias="forceReextract")


ExtractedProfile = CompanyProfileExtract | MentorProfileExtract


class ExtractedProfileDocument(CamelModel):
    actor_type: ExtractionActorType = Field(alias="actorType")
    actor_id: str = Field(alias="actorId")
    display_name: str | None = Field(default=None, alias="displayName")
    raw_profile_text: str = Field(alias="rawProfileText")
    extracted_profile: dict[str, Any] = Field(alias="extractedProfile")
    extraction_status: ExtractionStatus = Field(alias="extractionStatus")
    extraction_confidence: float = Field(ge=0, le=1, alias="extractionConfidence")
    profile_version: int = Field(default=1, ge=1, alias="profileVersion")
    created_at: datetime = Field(default_factory=utc_now, alias="createdAt")
    updated_at: datetime = Field(default_factory=utc_now, alias="updatedAt")


class ExtractionLog(CamelModel):
    log_id: str = Field(alias="logId")
    actor_type: ExtractionActorType = Field(alias="actorType")
    actor_id: str = Field(alias="actorId")
    status: ExtractionStatus
    raw_profile_text_hash: str = Field(alias="rawProfileTextHash")
    model: str
    prompt_version: str = Field(alias="promptVersion")
    confidence_score: float | None = Field(default=None, ge=0, le=1, alias="confidenceScore")
    missing_fields: list[str] = Field(default_factory=list, alias="missingFields")
    error_code: str | None = Field(default=None, alias="errorCode")
    error_message: str | None = Field(default=None, alias="errorMessage")
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(default_factory=utc_now, alias="createdAt")


class ProfileExtractionResponse(CamelModel):
    actor_type: ExtractionActorType = Field(alias="actorType")
    actor_id: str = Field(alias="actorId")
    extraction_status: ExtractionStatus = Field(alias="extractionStatus")
    extraction_confidence: float = Field(ge=0, le=1, alias="extractionConfidence")
    extracted_profile: ExtractedProfile = Field(alias="extractedProfile")
    missing_fields: list[str] = Field(default_factory=list, alias="missingFields")
    log_id: str = Field(alias="logId")
    profile_version: int = Field(alias="profileVersion")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


ExtractionModelType = Literal["company", "mentor"]
