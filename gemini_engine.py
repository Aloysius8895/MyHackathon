import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")


def _build_actor_summary(actor: dict) -> str:
    skills = ", ".join(actor.get("skills", [])) if actor.get("skills") else "N/A"
    return (
        f"Name: {actor['name']}\n"
        f"Type: {actor['type']}\n"
        f"Industry: {actor.get('industry', 'N/A')}\n"
        f"Location: {actor.get('location', 'N/A')}\n"
        f"Skills/Expertise: {skills}\n"
        f"Description: {actor.get('description', 'N/A')}"
    )


def find_matches(target_actor: dict, candidate_actors: list, programme: str = "", top_n: int = 5) -> list:
    """
    Use Gemini to rank candidate_actors against target_actor.
    Returns list of dicts: {actor_id, name, score, reason, confidence, bias_flag}
    """
    if not candidate_actors:
        return []

    candidates_text = "\n\n".join([
        f"CANDIDATE {i+1} (ID:{a['id']}):\n{_build_actor_summary(a)}"
        for i, a in enumerate(candidate_actors)
    ])

    prompt = f"""You are an AI ecosystem relationship manager for an innovation programme platform.

Your task is to evaluate and rank candidate actors for a match with the target actor below.
Programme context: {programme if programme else 'General innovation programme'}

TARGET ACTOR:
{_build_actor_summary(target_actor)}

CANDIDATES TO EVALUATE:
{candidates_text}

For each candidate, provide:
1. A match score from 0.0 to 1.0 (1.0 = perfect match)
2. A concise reason explaining WHY this match is valuable (2-3 sentences)
3. A confidence level: "high", "medium", or "low"
4. Any bias flag if the same candidate dominates too many matches (true/false)

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "actor_id": <integer id>,
    "name": "<name>",
    "score": <float 0.0-1.0>,
    "reason": "<why this match is good>",
    "confidence": "<high|medium|low>",
    "bias_flag": <true|false>
  }}
]

Rank by score descending. Return top {top_n} candidates only. Return ONLY the JSON array, no other text."""

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Strip markdown code blocks if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        results = json.loads(raw)
        return results[:top_n]

    except Exception as e:
        return [{"error": str(e)}]


def explain_linkage(actor_a: dict, actor_b: dict, engagement_history: list) -> str:
    """Generate a natural language explanation of why this linkage exists and its health."""
    history_text = ""
    if engagement_history:
        history_text = "\n".join([
            f"- Outcome: {e['outcome']}, Rating: {e['rating']}/5, Notes: {e['notes']}"
            for e in engagement_history
        ])
    else:
        history_text = "No engagement history yet."

    prompt = f"""You are an ecosystem relationship analyst.

Explain this ecosystem linkage in 3-4 sentences:
- What value does this relationship create?
- Based on engagement history, how healthy is this linkage?
- What should be done to strengthen or evolve it?

ACTOR A:
{_build_actor_summary(actor_a)}

ACTOR B:
{_build_actor_summary(actor_b)}

ENGAGEMENT HISTORY:
{history_text}

Be concise, practical, and actionable. Do not use bullet points."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate explanation: {e}"


def suggest_programme_matches(companies: list, mentors: list, programme: str) -> str:
    """High-level AI summary of the best overall matches for a programme."""
    if not companies or not mentors:
        return "Not enough actors to generate programme suggestions."

    companies_text = "\n".join([f"- {c['name']} ({c.get('industry','')}, {c.get('location','')})" for c in companies[:10]])
    mentors_text = "\n".join([f"- {m['name']} (Skills: {', '.join(m.get('skills',[])[:3])})" for m in mentors[:10]])

    prompt = f"""You are an innovation ecosystem coordinator for '{programme}'.

Given these companies and mentors, provide 3 high-priority match recommendations.
For each recommendation explain the strategic value in 2 sentences.

COMPANIES:
{companies_text}

MENTORS:
{mentors_text}

Format your response as:
1. [Company] ↔ [Mentor]: <reason>
2. [Company] ↔ [Mentor]: <reason>
3. [Company] ↔ [Mentor]: <reason>

Then add one paragraph on overall ecosystem health and diversity."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate suggestions: {e}"
