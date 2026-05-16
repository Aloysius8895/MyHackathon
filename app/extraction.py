import asyncio
import hashlib
import json
import re
from typing import Any, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ValidationError

from app.config import Settings
from app.models import (
    AvailabilityStatus,
    CompanyExtractionRequest,
    CompanyProfileExtract,
    ExtractedProfile,
    ExtractedProfileDocument,
    ExtractionActorType,
    ExtractionLog,
    ExtractionStatus,
    MentorExtractionRequest,
    MentorProfileExtract,
    NormalizedProfile,
    ProfileExtractionResponse,
    ProfileType,
    utc_now,
)
from app.repositories import Repository
from app.scoring import text_embedding, tokenize


PROMPT_VERSION = "profile-extraction-v1"

TExtract = TypeVar("TExtract", CompanyProfileExtract, MentorProfileExtract)


def _enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


class DuplicateExtractionError(Exception):
    pass


class ExtractionValidationError(Exception):
    pass


class GeminiExtractionError(Exception):
    pass


class ProfileNotFoundError(Exception):
    pass


def build_grounded_extraction_prompt(actor_type: ExtractionActorType, schema: dict, raw_profile_text: str) -> str:
    return f"""
You are an information extraction system for an innovation ecosystem platform.

Your task is to extract structured data from the provided profile text.

Rules:
- Output valid JSON only.
- Do not include markdown.
- Do not include explanations outside JSON.
- Use only the provided profile text.
- Do not invent facts.
- If a value is not stated or cannot be safely inferred, use null, "unknown", or [].
- Include confidenceScore from 0.0 to 1.0.
- Include missingFields for important fields not found.
- Include extractionNotes explaining uncertainty using only provided text.

Actor type:
{actor_type.value}

Expected JSON schema:
{json.dumps(schema, indent=2)}

Profile text:
\"\"\"
{raw_profile_text}
\"\"\"
""".strip()


def parse_json_object(raw_response: str) -> dict:
    try:
        value = json.loads(raw_response)
    except json.JSONDecodeError:
        fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_response, re.DOTALL)
        object_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
        candidate = fenced_match.group(1) if fenced_match else object_match.group(0) if object_match else None
        if not candidate:
            raise
        value = json.loads(candidate)
    if not isinstance(value, dict):
        raise json.JSONDecodeError("Gemini response must be a JSON object", raw_response, 0)
    return value


def raw_text_hash(raw_profile_text: str) -> str:
    return hashlib.sha256(raw_profile_text.encode("utf-8")).hexdigest()


class GeminiExtractionClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate_json(self, prompt: str) -> str:
        return await asyncio.to_thread(self._generate_json_sync, prompt)

    def _generate_json_sync(self, prompt: str) -> str:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise GeminiExtractionError("google-genai is not installed") from exc

        if self.settings.gemini_api_key:
            client = genai.Client(api_key=self.settings.gemini_api_key)
        elif self.settings.google_cloud_project:
            client = genai.Client(
                vertexai=True,
                project=self.settings.google_cloud_project,
                location=self.settings.google_cloud_location,
            )
        else:
            raise GeminiExtractionError("No Gemini credentials: set GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT")

        try:
            response = client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=self.settings.gemini_temperature,
                ),
            )
        except Exception as exc:
            raise GeminiExtractionError(f"Gemini request failed: {exc}") from exc
        if not response.text:
            raise GeminiExtractionError("Gemini returned an empty response")
        return response.text


class LlmProfileExtractionService:
    def __init__(self, repository: Repository, settings: Settings) -> None:
        self.repository = repository
        self.settings = settings
        self.gemini_client = GeminiExtractionClient(settings)

    async def extract_company(self, request: CompanyExtractionRequest, admin_id: str) -> ProfileExtractionResponse:
        existing = await self.repository.get_extracted_actor(ExtractionActorType.company, request.company_id)
        if existing and not request.force_reextract:
            raise DuplicateExtractionError("Company profile has already been extracted")

        try:
            extract = await self._extract(
                actor_type=ExtractionActorType.company,
                raw_profile_text=request.raw_profile_text,
                output_model=CompanyProfileExtract,
            )
        except (ExtractionValidationError, GeminiExtractionError) as exc:
            await self._write_failure_log(ExtractionActorType.company, request.company_id, request.raw_profile_text, admin_id, exc)
            raise
        display_name = request.display_name or extract.company_name
        return await self._save_result(
            actor_type=ExtractionActorType.company,
            actor_id=request.company_id,
            display_name=display_name,
            raw_profile_text=request.raw_profile_text,
            extracted_profile=extract,
            existing=existing,
            admin_id=admin_id,
        )

    async def extract_mentor(self, request: MentorExtractionRequest, admin_id: str) -> ProfileExtractionResponse:
        existing = await self.repository.get_extracted_actor(ExtractionActorType.mentor, request.mentor_id)
        if existing and not request.force_reextract:
            raise DuplicateExtractionError("Mentor profile has already been extracted")

        try:
            extract = await self._extract(
                actor_type=ExtractionActorType.mentor,
                raw_profile_text=request.raw_profile_text,
                output_model=MentorProfileExtract,
            )
        except (ExtractionValidationError, GeminiExtractionError) as exc:
            await self._write_failure_log(ExtractionActorType.mentor, request.mentor_id, request.raw_profile_text, admin_id, exc)
            raise
        display_name = request.display_name or extract.mentor_name
        return await self._save_result(
            actor_type=ExtractionActorType.mentor,
            actor_id=request.mentor_id,
            display_name=display_name,
            raw_profile_text=request.raw_profile_text,
            extracted_profile=extract,
            existing=existing,
            admin_id=admin_id,
        )

    async def get_extracted_profile(self, actor_type: ExtractionActorType, actor_id: str) -> ProfileExtractionResponse:
        document = await self.repository.get_extracted_actor(actor_type, actor_id)
        if not document:
            raise ProfileNotFoundError(f"{actor_type.value} profile extraction not found")
        latest_log = await self.repository.get_latest_extraction_log(actor_type, actor_id)
        return self._to_response(document, latest_log.log_id if latest_log else "")

    async def _extract(self, actor_type: ExtractionActorType, raw_profile_text: str, output_model: type[TExtract]) -> TExtract:
        has_credentials = bool(self.settings.gemini_api_key or self.settings.google_cloud_project)
        if self.settings.ai_provider == "gemini":
            if not has_credentials:
                raise GeminiExtractionError("No Gemini credentials: set GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT")
            schema = output_model.model_json_schema(by_alias=True)
            prompt = build_grounded_extraction_prompt(actor_type, schema, raw_profile_text)
            try:
                raw_response = await self.gemini_client.generate_json(prompt)
                payload = parse_json_object(raw_response)
                return output_model.model_validate(payload)
            except (json.JSONDecodeError, ValidationError) as exc:
                raise ExtractionValidationError("Gemini response did not match the extraction schema") from exc
        return self._heuristic_extract(actor_type, raw_profile_text, output_model)

    def _heuristic_extract(self, actor_type: ExtractionActorType, raw_profile_text: str, output_model: type[TExtract]) -> TExtract:
        tokens = tokenize(raw_profile_text)
        industries = self._find_terms(tokens, {
            "FinTech": {"fintech", "finance", "payments", "banking"},
            "HealthTech": {"health", "medical", "patient"},
            "Manufacturing": {"manufacturing", "factory", "industrial", "iot"},
            "Climate": {"climate", "energy", "carbon", "sustainability"},
            "SaaS": {"saas", "software", "platform"},
        })
        needs = self._find_terms(tokens, {
            "Fundraising": {"fundraising", "capital", "investment", "venture", "seed", "vc"},
            "Go-to-market": {"marketing", "sales", "growth", "gtm", "market"},
            "Product strategy": {"product", "roadmap", "ux"},
            "Technical architecture": {"architecture", "backend", "cloud", "ai"},
            "Partnerships": {"partner", "partnership", "channel", "ecosystem"},
        })
        stage = self._find_stage(tokens)
        country = self._find_country(raw_profile_text)
        confidence = self._estimate_confidence([industries, needs, [stage] if stage else [], [country] if country else []])

        if actor_type == ExtractionActorType.company:
            payload = {
                "companyName": self._guess_name(raw_profile_text) or "unknown",
                "industry": industries,
                "stage": stage or "Unknown",
                "needs": needs,
                "country": country or "unknown",
                "targetMarket": self._find_target_market(raw_profile_text),
                "businessModel": self._find_terms(tokens, {"SaaS": {"saas"}, "Transaction fees": {"transaction", "fees"}, "Marketplace": {"marketplace"}}),
                "preferredSupportTypes": self._support_types(needs),
                "programmeInterest": [],
                "confidenceScore": confidence,
                "missingFields": self._missing_fields({
                    "companyName": True,
                    "industry": bool(industries),
                    "stage": bool(stage),
                    "needs": bool(needs),
                    "country": bool(country),
                    "targetMarket": bool(self._find_target_market(raw_profile_text)),
                    "businessModel": "saas" in tokens or "transaction" in tokens or "marketplace" in tokens,
                }),
                "extractionNotes": "Heuristic local extraction used because AI_PROVIDER is not set to gemini.",
            }
        else:
            payload = {
                "mentorName": self._guess_name(raw_profile_text) or "unknown",
                "industries": industries,
                "expertise": needs,
                "stageExperience": [stage] if stage else [],
                "country": country or "unknown",
                "availability": self._find_availability(tokens),
                "maxCapacity": self._find_capacity(raw_profile_text),
                "currentCapacity": 0,
                "pastExperience": self._past_experience(raw_profile_text),
                "preferredCompanyTypes": industries,
                "confidenceScore": confidence,
                "missingFields": self._missing_fields({
                    "mentorName": True,
                    "industries": bool(industries),
                    "expertise": bool(needs),
                    "stageExperience": bool(stage),
                    "country": bool(country),
                    "availability": True,
                    "maxCapacity": self._find_capacity(raw_profile_text) is not None,
                }),
                "extractionNotes": "Heuristic local extraction used because AI_PROVIDER is not set to gemini.",
            }
        return output_model.model_validate(payload)

    async def _save_result(
        self,
        actor_type: ExtractionActorType,
        actor_id: str,
        display_name: str | None,
        raw_profile_text: str,
        extracted_profile: ExtractedProfile,
        existing: ExtractedProfileDocument | None,
        admin_id: str,
    ) -> ProfileExtractionResponse:
        status = ExtractionStatus.completed
        if extracted_profile.confidence_score < self.settings.extraction_confidence_threshold:
            status = ExtractionStatus.needs_review
        now = utc_now()
        profile_version = (existing.profile_version + 1) if existing else 1
        document = ExtractedProfileDocument(
            actorType=actor_type,
            actorId=actor_id,
            displayName=display_name,
            rawProfileText=raw_profile_text,
            extractedProfile=extracted_profile.model_dump(by_alias=True),
            extractionStatus=status,
            extractionConfidence=extracted_profile.confidence_score,
            profileVersion=profile_version,
            createdAt=existing.created_at if existing else now,
            updatedAt=now,
        )
        log = ExtractionLog(
            logId=f"log_{uuid4().hex[:12]}",
            actorType=actor_type,
            actorId=actor_id,
            status=status,
            rawProfileTextHash=raw_text_hash(raw_profile_text),
            model=self.settings.gemini_model if self.settings.ai_provider == "gemini" else "heuristic-local",
            promptVersion=PROMPT_VERSION,
            confidenceScore=extracted_profile.confidence_score,
            missingFields=extracted_profile.missing_fields,
            createdBy=admin_id,
        )
        normalized_profile = self._to_normalized_profile(document)
        await self.repository.save_extracted_actor(document, normalized_profile)
        await self.repository.write_extraction_log(log)
        return self._to_response(document, log.log_id)

    async def _write_failure_log(
        self,
        actor_type: ExtractionActorType,
        actor_id: str,
        raw_profile_text: str,
        admin_id: str,
        exc: Exception,
    ) -> None:
        status = ExtractionStatus.failed_invalid_json if isinstance(exc, ExtractionValidationError) else ExtractionStatus.failed_validation
        log = ExtractionLog(
            logId=f"log_{uuid4().hex[:12]}",
            actorType=actor_type,
            actorId=actor_id,
            status=status,
            rawProfileTextHash=raw_text_hash(raw_profile_text),
            model=self.settings.gemini_model if self.settings.ai_provider == "gemini" else "heuristic-local",
            promptVersion=PROMPT_VERSION,
            confidenceScore=None,
            missingFields=[],
            errorCode=status.value,
            errorMessage=str(exc),
            createdBy=admin_id,
        )
        await self.repository.write_extraction_log(log)

    def _to_response(self, document: ExtractedProfileDocument, log_id: str) -> ProfileExtractionResponse:
        extracted_profile = self._parse_document_profile(document)
        return ProfileExtractionResponse(
            actorType=document.actor_type,
            actorId=document.actor_id,
            extractionStatus=document.extraction_status,
            extractionConfidence=document.extraction_confidence,
            extractedProfile=extracted_profile,
            missingFields=extracted_profile.missing_fields,
            logId=log_id,
            profileVersion=document.profile_version,
            createdAt=document.created_at,
            updatedAt=document.updated_at,
        )

    def _to_normalized_profile(self, document: ExtractedProfileDocument) -> NormalizedProfile:
        if document.actor_type == ExtractionActorType.company:
            extract = CompanyProfileExtract.model_validate(document.extracted_profile)
            return NormalizedProfile(
                profile_id=document.actor_id,
                profile_type=ProfileType.company,
                display_name=document.display_name or extract.company_name or document.actor_id,
                industry=extract.industry,
                stage=str(extract.stage or "Unknown"),
                needs=extract.needs,
                country=extract.country,
                verified=False,
                tags=sorted(tokenize(extract.industry + extract.needs + extract.business_model)),
                embedding=text_embedding(extract.industry + extract.needs + extract.target_market + extract.business_model),
                metadata={
                    "rawProfileText": document.raw_profile_text,
                    "extractedProfile": extract.model_dump(by_alias=True),
                    "extractionStatus": _enum_value(document.extraction_status),
                    "profileVersion": document.profile_version,
                },
            )
        extract = MentorProfileExtract.model_validate(document.extracted_profile)
        is_available = extract.availability in {AvailabilityStatus.available, "available", AvailabilityStatus.limited, "limited"}
        return NormalizedProfile(
            profile_id=document.actor_id,
            profile_type=ProfileType.mentor,
            display_name=document.display_name or extract.mentor_name or document.actor_id,
            industry=extract.industries,
            stage=extract.stage_experience[0] if extract.stage_experience else None,
            expertise=extract.expertise,
            country=extract.country,
            availability=is_available,
            capacity=extract.max_capacity or 0,
            active_assignments=extract.current_capacity,
            past_experience=extract.past_experience,
            verified=False,
            tags=sorted(tokenize(extract.industries + extract.expertise + extract.preferred_company_types)),
            embedding=text_embedding(extract.industries + extract.expertise + extract.past_experience + extract.preferred_company_types),
            metadata={
                "rawProfileText": document.raw_profile_text,
                "extractedProfile": extract.model_dump(by_alias=True),
                "extractionStatus": _enum_value(document.extraction_status),
                "profileVersion": document.profile_version,
            },
        )

    def _parse_document_profile(self, document: ExtractedProfileDocument) -> ExtractedProfile:
        if document.actor_type == ExtractionActorType.company:
            return CompanyProfileExtract.model_validate(document.extracted_profile)
        return MentorProfileExtract.model_validate(document.extracted_profile)

    def _find_terms(self, tokens: set[str], mapping: dict[str, set[str]]) -> list[str]:
        return [label for label, keywords in mapping.items() if tokens.intersection(keywords)]

    def _find_stage(self, tokens: set[str]) -> str | None:
        stage_map = {
            "Idea": {"idea", "concept"},
            "MVP": {"mvp", "prototype", "pilot"},
            "Pre-seed": {"preseed", "pre", "early"},
            "Seed": {"seed"},
            "Series A": {"series"},
            "Growth": {"growth", "scale", "scaling"},
        }
        return next((stage for stage, keywords in stage_map.items() if tokens.intersection(keywords)), None)

    def _find_country(self, raw_profile_text: str) -> str | None:
        lower_text = raw_profile_text.casefold()
        for country in ["Malaysia", "Singapore", "Indonesia", "Thailand", "Vietnam", "United Kingdom"]:
            if country.casefold() in lower_text:
                return country
        return None

    def _guess_name(self, raw_profile_text: str) -> str | None:
        first_sentence = raw_profile_text.strip().split(".")[0]
        words = first_sentence.split()
        if len(words) < 2:
            return None
        return " ".join(words[: min(3, len(words))]).strip(",")

    def _find_target_market(self, raw_profile_text: str) -> list[str]:
        lower_text = raw_profile_text.casefold()
        markets: list[str] = []
        if "sme" in lower_text:
            markets.append("SMEs")
        if "enterprise" in lower_text:
            markets.append("Enterprise")
        if "southeast asia" in lower_text or "asean" in lower_text:
            markets.append("Southeast Asia")
        return markets

    def _support_types(self, needs: list[str]) -> list[str]:
        support_types: list[str] = []
        if "Fundraising" in needs:
            support_types.extend(["Mentorship", "Investor introductions"])
        if "Go-to-market" in needs:
            support_types.append("Go-to-market mentorship")
        if "Partnerships" in needs:
            support_types.append("Partner introductions")
        return support_types

    def _find_availability(self, tokens: set[str]) -> str:
        if {"unavailable", "busy"}.intersection(tokens):
            return "unavailable"
        if {"limited", "quarter"}.intersection(tokens):
            return "limited"
        if {"available", "availability"}.intersection(tokens):
            return "available"
        return "unknown"

    def _find_capacity(self, raw_profile_text: str) -> int | None:
        match = re.search(r"\b(?:for|with|take|support)?\s*(\d+)\s+(?:active\s+)?(?:mentees|companies|startups|founders|slots)\b", raw_profile_text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def _past_experience(self, raw_profile_text: str) -> list[str]:
        sentences = [sentence.strip() for sentence in raw_profile_text.split(".") if sentence.strip()]
        return [sentence for sentence in sentences if any(word in sentence.casefold() for word in ["former", "mentored", "built", "led", "helped"])][:3]

    def _estimate_confidence(self, groups: list[list[str]]) -> float:
        present = sum(1 for group in groups if group)
        return round(min(0.35 + (present * 0.15), 0.95), 2)

    def _missing_fields(self, fields: dict[str, bool]) -> list[str]:
        return [field for field, is_present in fields.items() if not is_present]
