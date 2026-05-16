import re
from pathlib import Path

from fastapi import UploadFile

from app.config import Settings
from app.extraction import (
    DuplicateExtractionError,
    ExtractionValidationError,
    GeminiExtractionError,
    LlmProfileExtractionService,
)
from app.file_ingestion import FileIngestionError, extract_upload_text
from app.models import (
    CompanyExtractionRequest,
    ExtractionActorType,
    MatchRunRequest,
    MatchRunResponse,
    MentorExtractionRequest,
    ProfileType,
    WorkflowIngestionResult,
    WorkflowMatchResult,
    WorkflowRunResponse,
)
from app.reports import GeminiReportService
from app.repositories import Repository
from app.services import MatchingService


async def run_uploaded_matching_workflow(
    repository: Repository,
    settings: Settings,
    company_files: list[UploadFile] | None,
    mentor_files: list[UploadFile] | None,
    limit: int,
    admin_id: str,
) -> WorkflowRunResponse:
    ingested: list[WorkflowIngestionResult] = []
    extraction_service = LlmProfileExtractionService(repository, settings)

    for file in company_files or []:
        ingested.append(await _ingest_file(repository, settings, extraction_service, file, ExtractionActorType.company, admin_id))
    for file in mentor_files or []:
        ingested.append(await _ingest_file(repository, settings, extraction_service, file, ExtractionActorType.mentor, admin_id))

    company_ids = [
        item.actor_id
        for item in ingested
        if item.actor_type == ExtractionActorType.company and item.actor_id and item.status == "ingested"
    ]
    if not company_ids:
        company_ids = [company.profile_id for company in await repository.list_companies() if company.verified]

    match_results, match_runs = await _run_matches(repository, company_ids, limit)
    report, report_source = await GeminiReportService(repository, settings).generate_matching_report(match_runs)
    return WorkflowRunResponse(
        ingested=ingested,
        matches=match_results,
        report=report,
        reportSource=report_source,
    )


async def _ingest_file(
    repository: Repository,
    settings: Settings,
    extraction_service: LlmProfileExtractionService,
    file: UploadFile,
    actor_type: ExtractionActorType,
    admin_id: str,
) -> WorkflowIngestionResult:
    file_name = file.filename or "uploaded-file"
    try:
        upload = await extract_upload_text(file)
        actor_id = _actor_id(actor_type, upload.file_name)
        display_name = _display_name(upload.file_name)
        raw_text = upload.text[: settings.max_profile_text_chars]

        if actor_type == ExtractionActorType.company:
            response = await extraction_service.extract_company(
                CompanyExtractionRequest(
                    companyId=actor_id,
                    displayName=display_name,
                    rawProfileText=raw_text,
                    forceReextract=True,
                ),
                admin_id=admin_id,
            )
        else:
            response = await extraction_service.extract_mentor(
                MentorExtractionRequest(
                    mentorId=actor_id,
                    displayName=display_name,
                    rawProfileText=raw_text,
                    forceReextract=True,
                ),
                admin_id=admin_id,
            )

        profile = await repository.get_profile(actor_id)
        if profile:
            profile.verified = True
            profile.metadata = {
                **profile.metadata,
                "sourceFileName": upload.file_name,
                "sourceContentType": upload.content_type,
                "workflowAutoVerified": True,
            }
            if profile.profile_type == ProfileType.mentor:
                profile.availability = True
                profile.capacity = max(profile.capacity, 3)
            await repository.save_profile(profile)

        return WorkflowIngestionResult(
            fileName=upload.file_name,
            actorType=actor_type,
            actorId=actor_id,
            displayName=display_name,
            status="ingested",
            extractionStatus=response.extraction_status,
            extractionConfidence=response.extraction_confidence,
            vectorDimensions=len(profile.embedding) if profile else 0,
            missingFields=response.missing_fields,
        )
    except (DuplicateExtractionError, ExtractionValidationError, GeminiExtractionError, FileIngestionError, ValueError) as exc:
        return WorkflowIngestionResult(
            fileName=file_name,
            actorType=actor_type,
            status="failed",
            error=str(exc),
        )


async def _run_matches(
    repository: Repository,
    company_ids: list[str],
    limit: int,
) -> tuple[list[WorkflowMatchResult], list[MatchRunResponse]]:
    matching_service = MatchingService(repository)
    match_results: list[WorkflowMatchResult] = []
    match_runs: list[MatchRunResponse] = []

    for company_id in company_ids:
        company = await repository.get_profile(company_id)
        display_name = company.display_name if company else company_id
        try:
            match_run = await matching_service.run_company_to_mentor_match(
                MatchRunRequest(company_id=company_id, limit=limit, persist_recommendations=True)
            )
        except ValueError as exc:
            match_results.append(
                WorkflowMatchResult(
                    companyId=company_id,
                    displayName=display_name,
                    recommendations=[],
                    error=str(exc),
                )
            )
            continue

        match_runs.append(match_run)
        match_results.append(
            WorkflowMatchResult(
                companyId=company_id,
                displayName=display_name,
                recommendations=match_run.recommendations,
            )
        )
    return match_results, match_runs


def _actor_id(actor_type: ExtractionActorType, file_name: str) -> str:
    prefix = "cmp" if actor_type == ExtractionActorType.company else "men"
    stem = Path(file_name).stem.casefold()
    normalized = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    return f"{prefix}_{normalized or 'uploaded'}"[:120]


def _display_name(file_name: str) -> str:
    stem = Path(file_name).stem.replace("_", " ").replace("-", " ").strip()
    return re.sub(r"\s+", " ", stem).title() or "Uploaded Profile"
