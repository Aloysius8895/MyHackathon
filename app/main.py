from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app.ai import ProfileExtractor
from app.auth import require_admin
from app.config import Settings, get_settings
from app.models import (
    AuthContext,
    FeedbackRequest,
    MatchRunRequest,
    MatchRunResponse,
    NormalizedProfile,
    ProfileExtractionRequest,
    Recommendation,
    RecommendationDecisionRequest,
    RecommendationStatus,
    Relationship,
    RelationshipStatus,
)
from app.repositories import FirestoreRepository, InMemoryRepository, Repository
from app.routes.profile_extraction import router as profile_extraction_router
from app.services import MatchingService, mark_recommendation_decision


def build_repository(settings: Settings) -> Repository:
    if settings.storage_backend == "firestore":
        return FirestoreRepository()
    return InMemoryRepository(seed_demo_data=True)


def create_app(repository: Repository | None = None, settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    resolved_repository = repository or build_repository(resolved_settings)
    profile_extractor = ProfileExtractor()

    @asynccontextmanager
    async def lifespan(api: FastAPI):
        api.state.settings = resolved_settings
        api.state.repository = resolved_repository
        api.state.profile_extractor = profile_extractor
        yield

    api = FastAPI(
        title=resolved_settings.app_name,
        description="Backend-only Hybrid AI Relationship Matching Engine for ecosystem linkages.",
        version="0.1.0",
        lifespan=lifespan,
    )
    api.state.settings = resolved_settings
    api.state.repository = resolved_repository
    api.state.profile_extractor = profile_extractor
    api.include_router(profile_extraction_router)

    @api.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "matching-engine"}

    @api.post("/profiles/extract", response_model=NormalizedProfile, status_code=status.HTTP_201_CREATED)
    async def extract_profile(
        request: ProfileExtractionRequest,
        auth_context: AuthContext = Depends(require_admin),
    ) -> NormalizedProfile:
        del auth_context
        profile = await api.state.profile_extractor.extract(request)
        return await api.state.repository.save_profile(profile)

    @api.post("/matches/run", response_model=MatchRunResponse)
    async def run_match(
        request: MatchRunRequest,
        auth_context: AuthContext = Depends(require_admin),
    ) -> MatchRunResponse:
        del auth_context
        try:
            return await MatchingService(api.state.repository).run_company_to_mentor_match(request)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    @api.get("/recommendations", response_model=list[Recommendation])
    async def list_recommendations(
        status_filter: RecommendationStatus | None = Query(default=None, alias="status"),
        auth_context: AuthContext = Depends(require_admin),
    ) -> list[Recommendation]:
        del auth_context
        return await api.state.repository.list_recommendations(status_filter)

    @api.post("/recommendations/{recommendation_id}/approve", response_model=Relationship)
    async def approve_recommendation(
        recommendation_id: str,
        request: RecommendationDecisionRequest,
        auth_context: AuthContext = Depends(require_admin),
    ) -> Relationship:
        del auth_context
        recommendation = await _get_pending_recommendation(api.state.repository, recommendation_id)
        relationship = await MatchingService(api.state.repository).create_relationship_from_recommendation(
            recommendation,
            admin_id=request.admin_id,
        )
        updated = mark_recommendation_decision(recommendation, RecommendationStatus.accepted, request.admin_id, request.note)
        await api.state.repository.save_recommendation(updated)
        return relationship

    @api.post("/recommendations/{recommendation_id}/reject", response_model=Recommendation)
    async def reject_recommendation(
        recommendation_id: str,
        request: RecommendationDecisionRequest,
        auth_context: AuthContext = Depends(require_admin),
    ) -> Recommendation:
        del auth_context
        recommendation = await _get_pending_recommendation(api.state.repository, recommendation_id)
        updated = mark_recommendation_decision(recommendation, RecommendationStatus.rejected, request.admin_id, request.note)
        return await api.state.repository.save_recommendation(updated)

    @api.post("/recommendations/{recommendation_id}/override", response_model=Relationship)
    async def override_recommendation(
        recommendation_id: str,
        request: RecommendationDecisionRequest,
        auth_context: AuthContext = Depends(require_admin),
    ) -> Relationship:
        del auth_context
        if not request.override_mentor_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="override_mentor_id is required")
        recommendation = await _get_pending_recommendation(api.state.repository, recommendation_id)
        try:
            relationship = await MatchingService(api.state.repository).create_relationship_from_recommendation(
                recommendation,
                admin_id=request.admin_id,
                mentor_id=request.override_mentor_id,
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        updated = mark_recommendation_decision(
            recommendation,
            RecommendationStatus.overridden,
            request.admin_id,
            request.note,
            request.override_mentor_id,
        )
        await api.state.repository.save_recommendation(updated)
        return relationship

    @api.get("/relationships", response_model=list[Relationship])
    async def list_relationships(
        status_filter: RelationshipStatus | None = Query(default=None, alias="status"),
        auth_context: AuthContext = Depends(require_admin),
    ) -> list[Relationship]:
        del auth_context
        return await api.state.repository.list_relationships(status_filter)

    @api.post("/relationships/{relationship_id}/feedback", response_model=Relationship)
    async def add_feedback(
        relationship_id: str,
        request: FeedbackRequest,
        auth_context: AuthContext = Depends(require_admin),
    ) -> Relationship:
        del auth_context
        try:
            return await api.state.repository.add_feedback(relationship_id, request)
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship not found") from exc

    return api


async def _get_pending_recommendation(repository: Repository, recommendation_id: str) -> Recommendation:
    recommendation = await repository.get_recommendation(recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if recommendation.status != RecommendationStatus.pending:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Recommendation is no longer pending")
    return recommendation


app = create_app()
