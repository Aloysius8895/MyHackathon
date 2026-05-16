from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.ai import ProfileExtractor
from app.auth import require_admin
from app.config import Settings, get_settings
from app.extraction import GeminiExtractionClient, GeminiExtractionError
from app.models import (
    AuthContext,
    FeedbackRequest,
    HistoryUpload,
    HistoryUploadSaveResponse,
    MatchRunRequest,
    MatchRunResponse,
    NormalizedProfile,
    ProfileExtractionRequest,
    ProfileType,
    Recommendation,
    RecommendationDecisionRequest,
    RecommendationStatus,
    Relationship,
    RelationshipStatus,
    WorkflowRunResponse,
    utc_now,
)
from app.reports import GeminiReportService
from app.repositories import FirestoreRepository, InMemoryRepository, Repository
from app.routes.profile_extraction import router as profile_extraction_router
from app.services import MatchingService, mark_recommendation_decision
from app.workflow import run_uploaded_matching_workflow


PROJECT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_DIR / "dist"
PUBLIC_DIR = PROJECT_DIR / "public"


def frontend_dir() -> Path:
    if (DIST_DIR / "index.html").exists():
        return DIST_DIR
    return PUBLIC_DIR


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
    api.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )
    api.state.settings = resolved_settings
    api.state.repository = resolved_repository
    api.state.profile_extractor = profile_extractor
    api.include_router(profile_extraction_router)
    static_assets = frontend_dir() / "assets"
    if static_assets.exists():
        api.mount("/assets", StaticFiles(directory=static_assets), name="frontend-assets")

    @api.get("/", include_in_schema=False)
    async def web_app() -> FileResponse:
        index_file = frontend_dir() / "index.html"
        if not index_file.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frontend not found")
        return FileResponse(index_file)

    @api.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "matching-engine"}

    @api.get("/ai/status")
    async def ai_status(
        auth_context: AuthContext = Depends(require_admin),
    ) -> dict[str, object]:
        del auth_context
        has_credentials = bool(resolved_settings.gemini_api_key or resolved_settings.google_cloud_project)
        payload: dict[str, object] = {
            "provider": resolved_settings.ai_provider,
            "model": resolved_settings.gemini_model,
            "configured": resolved_settings.ai_provider == "gemini" and has_credentials,
            "ok": False,
        }
        if resolved_settings.ai_provider != "gemini":
            return {**payload, "detail": "AI_PROVIDER is not set to gemini."}
        if not has_credentials:
            return {**payload, "detail": "Set GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT."}

        try:
            await GeminiExtractionClient(resolved_settings).generate_json(
                "Return the smallest valid JSON object with one boolean field named ok."
            )
        except GeminiExtractionError as exc:
            return {**payload, "detail": str(exc)}
        return {**payload, "ok": True, "detail": "Gemini request succeeded."}

    @api.get("/profiles", response_model=list[NormalizedProfile])
    async def list_profiles(
        profile_type: ProfileType | None = Query(default=None, alias="type"),
        auth_context: AuthContext = Depends(require_admin),
    ) -> list[NormalizedProfile]:
        del auth_context
        return await api.state.repository.list_profiles(profile_type)

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

    @api.post("/history/upload", response_model=HistoryUploadSaveResponse, status_code=status.HTTP_200_OK)
    async def upload_history(payload: HistoryUpload) -> HistoryUploadSaveResponse:
        record = payload.model_copy(update={"uploaded_at": utc_now()})
        await api.state.repository.save_history_upload(record.model_dump(mode="json", by_alias=True))
        return HistoryUploadSaveResponse(
            status="saved",
            companies=len(record.companies),
            mentors=len(record.mentors),
            engagements=len(record.engagements),
            uploaded_at=record.uploaded_at,
        )

    @api.get("/history/sessions")
    async def get_history_sessions() -> dict[str, object]:
        data = await api.state.repository.get_history_upload()
        return data or {}

    @api.get("/relationships", response_model=list[Relationship])
    async def list_relationships(
        status_filter: RelationshipStatus | None = Query(default=None, alias="status"),
        auth_context: AuthContext = Depends(require_admin),
    ) -> list[Relationship]:
        del auth_context
        return await api.state.repository.list_relationships(status_filter)

    @api.post("/workflow/run", response_model=WorkflowRunResponse)
    async def run_workflow(
        company_files: list[UploadFile] | None = File(default=None, description="Company/startup profile files"),
        mentor_files: list[UploadFile] | None = File(default=None, description="Mentor/advisor profile files"),
        limit: int = Form(default=5, ge=1, le=50),
        auth_context: AuthContext = Depends(require_admin),
    ) -> WorkflowRunResponse:
        return await run_uploaded_matching_workflow(
            repository=api.state.repository,
            settings=api.state.settings,
            company_files=company_files,
            mentor_files=mentor_files,
            limit=limit,
            admin_id=auth_context.user_id,
        )

    @api.get("/reports/matching")
    async def matching_report(
        limit: int = Query(default=5, ge=1, le=50),
        auth_context: AuthContext = Depends(require_admin),
    ) -> dict[str, str]:
        del auth_context
        match_runs: list[MatchRunResponse] = []
        matching_service = MatchingService(api.state.repository)
        for company in await api.state.repository.list_companies():
            if not company.verified:
                continue
            try:
                match_runs.append(
                    await matching_service.run_company_to_mentor_match(
                        MatchRunRequest(company_id=company.profile_id, limit=limit, persist_recommendations=False)
                    )
                )
            except ValueError:
                continue
        report, source = await GeminiReportService(api.state.repository, api.state.settings).generate_matching_report(match_runs)
        return {"report": report, "source": source}

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

    @api.get("/{frontend_path:path}", include_in_schema=False)
    async def frontend_app(frontend_path: str) -> FileResponse:
        root = frontend_dir()
        static_file = root / frontend_path
        if static_file.exists() and static_file.is_file():
            return FileResponse(static_file)
        index_file = root / "index.html"
        if not index_file.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frontend not found")
        return FileResponse(index_file)

    return api


async def _get_pending_recommendation(repository: Repository, recommendation_id: str) -> Recommendation:
    recommendation = await repository.get_recommendation(recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if recommendation.status != RecommendationStatus.pending:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Recommendation is no longer pending")
    return recommendation


app = create_app()
