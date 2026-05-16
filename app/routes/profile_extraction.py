from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.auth import require_admin
from app.config import Settings
from app.extraction import (
    DuplicateExtractionError,
    ExtractionValidationError,
    GeminiExtractionError,
    LlmProfileExtractionService,
    ProfileNotFoundError,
)
from app.models import (
    AuthContext,
    CompanyExtractionRequest,
    ExtractionActorType,
    MentorExtractionRequest,
    ProfileExtractionResponse,
)
from app.repositories import Repository


router = APIRouter(prefix="/profiles/extract", tags=["profile-extraction"])


def get_repository(request: Request) -> Repository:
    return request.app.state.repository


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_extraction_service(
    repository: Repository = Depends(get_repository),
    settings: Settings = Depends(get_settings),
) -> LlmProfileExtractionService:
    return LlmProfileExtractionService(repository, settings)


@router.post("/company", response_model=ProfileExtractionResponse, status_code=status.HTTP_201_CREATED)
async def extract_company_profile(
    request: CompanyExtractionRequest,
    auth_context: AuthContext = Depends(require_admin),
    service: LlmProfileExtractionService = Depends(get_extraction_service),
) -> ProfileExtractionResponse:
    try:
        return await service.extract_company(request, admin_id=auth_context.user_id)
    except DuplicateExtractionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ExtractionValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except GeminiExtractionError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.post("/mentor", response_model=ProfileExtractionResponse, status_code=status.HTTP_201_CREATED)
async def extract_mentor_profile(
    request: MentorExtractionRequest,
    auth_context: AuthContext = Depends(require_admin),
    service: LlmProfileExtractionService = Depends(get_extraction_service),
) -> ProfileExtractionResponse:
    try:
        return await service.extract_mentor(request, admin_id=auth_context.user_id)
    except DuplicateExtractionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ExtractionValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    except GeminiExtractionError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.get("/{actor_type}/{actor_id}", response_model=ProfileExtractionResponse)
async def get_extracted_profile(
    actor_type: ExtractionActorType,
    actor_id: str,
    auth_context: AuthContext = Depends(require_admin),
    service: LlmProfileExtractionService = Depends(get_extraction_service),
) -> ProfileExtractionResponse:
    del auth_context
    try:
        return await service.get_extracted_profile(actor_type, actor_id)
    except ProfileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
