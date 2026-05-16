import asyncio
import json
from datetime import date

from app.config import Settings
from app.models import MatchRunResponse, NormalizedProfile
from app.repositories import Repository


class GeminiReportService:
    def __init__(self, repository: Repository, settings: Settings) -> None:
        self.repository = repository
        self.settings = settings

    async def generate_matching_report(self, match_runs: list[MatchRunResponse]) -> tuple[str, str]:
        report_data = await self._build_report_data(match_runs)
        if not report_data:
            return "No matching results are available for report generation.", "none"
        return await asyncio.to_thread(self._call_gemini, report_data)

    async def _build_report_data(self, match_runs: list[MatchRunResponse]) -> list[dict]:
        rows: list[dict] = []
        for match_run in match_runs:
            company = await self.repository.get_profile(match_run.company_id)
            if not company:
                continue
            rows.append({
                "company": self._profile_summary(company),
                "top_matches": [
                    await self._recommendation_summary(recommendation)
                    for recommendation in match_run.recommendations
                ],
            })
        return rows

    async def _recommendation_summary(self, recommendation) -> dict:
        mentor = await self.repository.get_profile(recommendation.mentor_id)
        return {
            "mentor": self._profile_summary(mentor) if mentor else {"id": recommendation.mentor_id},
            "score": recommendation.match_score,
            "score_breakdown": recommendation.score_breakdown.model_dump(),
            "reason": recommendation.match_reason,
            "risk_note": recommendation.risk_note,
            "evidence": recommendation.evidence,
        }

    def _profile_summary(self, profile: NormalizedProfile) -> dict:
        return {
            "id": profile.profile_id,
            "name": profile.display_name,
            "type": profile.profile_type,
            "industry": profile.industry,
            "stage": profile.stage,
            "needs": profile.needs,
            "expertise": profile.expertise,
            "country": profile.country,
            "tags": profile.tags,
            "vector_dimensions": len(profile.embedding),
        }

    def _call_gemini(self, report_data: list[dict]) -> tuple[str, str]:
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            return self._fallback_report(report_data, "google-genai is not installed"), "fallback"

        if self.settings.gemini_api_key:
            client = genai.Client(api_key=self.settings.gemini_api_key)
        elif self.settings.google_cloud_project:
            client = genai.Client(
                vertexai=True,
                project=self.settings.google_cloud_project,
                location=self.settings.google_cloud_location,
            )
        else:
            return self._fallback_report(report_data, "No Gemini credentials configured"), "fallback"

        try:
            response = client.models.generate_content(
                model=self.settings.gemini_model,
                contents=self._build_prompt(report_data),
                config=types.GenerateContentConfig(temperature=0.3),
            )
        except Exception as exc:
            return self._fallback_report(report_data, f"Gemini request failed: {exc}"), "fallback"
        return response.text or self._fallback_report(report_data, "Gemini returned an empty response"), "gemini"

    def _build_prompt(self, report_data: list[dict]) -> str:
        today = date.today().strftime("%B %d, %Y")
        data_json = json.dumps(report_data, indent=2, ensure_ascii=False)
        return f"""You are an analyst for an innovation ecosystem matching platform.
Today's date: {today}

The backend has already extracted profiles, generated embeddings, computed match scores, and produced recommendation reasons.
Use the provided data only. Do not invent companies, mentors, scores, or facts.

Generate a concise executive report in Markdown with:
1. Executive Summary
2. Match Results by Company
3. Score and Vector Observations
4. Risks or Coverage Gaps
5. Recommended Admin Actions

Matching data:
```json
{data_json}
```
"""

    def _fallback_report(self, report_data: list[dict], reason: str) -> str:
        today = date.today().strftime("%B %d, %Y")
        lines = [f"# Matching Report - {today}", "", f"_Generated without Gemini: {reason}_", ""]
        for item in report_data:
            company = item["company"]
            lines.append(f"## {company['name']}")
            lines.append(f"- Profile: {', '.join(company.get('industry') or [])} | {company.get('stage') or 'Unknown'} | {company.get('country') or 'Unknown'}")
            lines.append(f"- Company vector dimensions: {company.get('vector_dimensions', 0)}")
            matches = item.get("top_matches") or []
            if not matches:
                lines.append("- No eligible mentor matches found.")
                lines.append("")
                continue
            for index, match in enumerate(matches, start=1):
                mentor = match["mentor"]
                lines.append(f"{index}. {mentor.get('name', mentor.get('id'))} - {match['score']:.2f}")
                lines.append(f"   - Reason: {match['reason']}")
                if match.get("risk_note"):
                    lines.append(f"   - Risk: {match['risk_note']}")
            lines.append("")
        return "\n".join(lines).strip()
