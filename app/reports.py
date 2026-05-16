import asyncio
import json
from datetime import date

from app.config import Settings
from app.models import MatchRunRequest
from app.repositories import Repository
from app.services import MatchingService


class GeminiReportService:
    def __init__(self, repository: Repository, settings: Settings) -> None:
        self.repository = repository
        self.settings = settings

    async def generate_matching_report(self) -> str:
        companies = await self.repository.list_companies()
        if not companies:
            return "No company profiles found in the database."

        matching_service = MatchingService(self.repository)
        results = []
        for company in companies:
            if not company.verified:
                continue
            try:
                response = await matching_service.run_company_to_mentor_match(
                    MatchRunRequest(company_id=company.profile_id, limit=3, persist_recommendations=False)
                )
                results.append({
                    "company": company.display_name,
                    "industry": company.industry,
                    "stage": company.stage,
                    "needs": company.needs,
                    "country": company.country,
                    "top_matches": [
                        {
                            "mentor": rec.mentor_display_name,
                            "score": rec.match_score,
                            "reason": rec.reason,
                            "risk_note": rec.risk_note,
                        }
                        for rec in response.recommendations
                    ],
                })
            except ValueError:
                continue

        if not results:
            return "No verified companies found for matching."

        return await asyncio.to_thread(self._call_gemini, results)

    def _call_gemini(self, results: list[dict]) -> str:
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            return self._fallback_report(results, "google-genai is not installed")

        if self.settings.gemini_api_key:
            client = genai.Client(api_key=self.settings.gemini_api_key)
        elif self.settings.google_cloud_project:
            client = genai.Client(
                vertexai=True,
                project=self.settings.google_cloud_project,
                location=self.settings.google_cloud_location,
            )
        else:
            return self._fallback_report(results, "No Gemini credentials configured")

        prompt = self._build_prompt(results)
        try:
            response = client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3),
            )
            return response.text or self._fallback_report(results, "Gemini returned an empty response")
        except Exception as exc:
            return self._fallback_report(results, f"Gemini request failed: {exc}")

    def _build_prompt(self, results: list[dict]) -> str:
        today = date.today().strftime("%B %d, %Y")
        data_json = json.dumps(results, indent=2, ensure_ascii=False)
        return f"""You are an analyst for an innovation ecosystem matching platform.
Today's date: {today}

Below is the output from our AI matching engine: companies paired with their top mentor candidates.
Generate a concise executive report in Markdown for the programme manager that includes:

1. Executive Summary: 2-3 sentences on overall ecosystem matching health
2. Match Results: for each company, list the top mentors with key reasons and any risk notes
3. Ecosystem Observations: patterns, coverage gaps, or notable mentor capacity issues
4. Recommended Actions: concrete next steps for the admin team

Keep it professional, clear, and actionable. Do not invent data beyond what is provided.

Matching Data:
```json
{data_json}
```
"""

    def _fallback_report(self, results: list[dict], reason: str = "unknown") -> str:
        today = date.today().strftime("%B %d, %Y")
        lines = [f"# Matching Report - {today}\n", f"_Generated without Gemini: {reason}_\n"]
        for item in results:
            lines.append(f"\n## {item['company']}")
            lines.append(f"- **Industry:** {', '.join(item['industry'])}")
            lines.append(f"- **Stage:** {item['stage']} | **Country:** {item['country']}")
            lines.append(f"- **Needs:** {', '.join(item['needs'])}\n")
            if item["top_matches"]:
                lines.append("**Top Mentor Matches:**")
                for i, match in enumerate(item["top_matches"], 1):
                    lines.append(f"{i}. {match['mentor']} - Score: {match['score']:.2f}")
                    lines.append(f"   {match['reason']}")
                    if match["risk_note"]:
                        lines.append(f"   Warning: {match['risk_note']}")
            else:
                lines.append("_No eligible mentors found._")
        return "\n".join(lines)
