from uuid import uuid4

from app.models import NormalizedProfile, ProfileExtractionRequest, ProfileType
from app.scoring import text_embedding, tokenize


INDUSTRY_KEYWORDS = {
    "FinTech": {"fintech", "finance", "financial", "banking", "payments"},
    "HealthTech": {"health", "medical", "clinic", "patient"},
    "Manufacturing": {"manufacturing", "factory", "industrial", "iot"},
    "Climate": {"climate", "sustainability", "carbon", "energy"},
    "SaaS": {"saas", "software", "platform", "subscription"},
}

NEED_KEYWORDS = {
    "Fundraising": {"fundraising", "fund", "investment", "venture", "capital", "seed"},
    "Go-to-market": {"sales", "marketing", "gtm", "customers", "growth"},
    "Product strategy": {"product", "roadmap", "ux", "user"},
    "Technical architecture": {"architecture", "cloud", "backend", "ai", "data"},
    "Partnerships": {"partner", "partnership", "ecosystem", "channel"},
}

STAGE_KEYWORDS = {
    "Idea": {"idea", "concept"},
    "MVP": {"mvp", "prototype", "pilot"},
    "Seed": {"seed", "early", "pre-seed"},
    "Growth": {"growth", "scale", "scaling"},
}


class ProfileExtractor:
    """Grounded extraction interface with a deterministic MVP fallback."""

    async def extract(self, request: ProfileExtractionRequest) -> NormalizedProfile:
        text = request.raw_text
        tokens = tokenize(text)
        industries = [name for name, keywords in INDUSTRY_KEYWORDS.items() if tokens.intersection(keywords)]
        extracted_needs = [name for name, keywords in NEED_KEYWORDS.items() if tokens.intersection(keywords)]
        stage = next((name for name, keywords in STAGE_KEYWORDS.items() if tokens.intersection(keywords)), None)
        country = self._extract_country(text)
        display_name = request.display_name or request.metadata.get("display_name") or "Extracted Profile"
        profile_id = request.profile_id or f"{request.profile_type.value}_{uuid4().hex[:10]}"
        is_mentor = request.profile_type == ProfileType.mentor

        return NormalizedProfile(
            profile_id=profile_id,
            profile_type=request.profile_type,
            display_name=display_name,
            industry=industries,
            stage=stage,
            needs=[] if is_mentor else extracted_needs,
            expertise=extracted_needs if is_mentor else [],
            country=country,
            availability=bool(request.metadata.get("availability", True)),
            programme_eligibility=request.metadata.get("programme_eligibility", []),
            capacity=int(request.metadata.get("capacity", 3 if is_mentor else 0)),
            active_assignments=int(request.metadata.get("active_assignments", 0)),
            past_experience=request.metadata.get("past_experience", []),
            verified=bool(request.metadata.get("verified", True)),
            conflicts=request.metadata.get("conflicts", []),
            tags=sorted(tokens.intersection({"fintech", "fundraising", "seed", "manufacturing", "growth", "ai", "saas"})),
            embedding=text_embedding([text]),
            metadata={**request.metadata, "raw_text": text},
        )

    def _extract_country(self, text: str) -> str | None:
        lower_text = text.casefold()
        for country in ["Malaysia", "Singapore", "Indonesia", "Thailand", "Vietnam", "United Kingdom"]:
            if country.casefold() in lower_text:
                return country
        return None
