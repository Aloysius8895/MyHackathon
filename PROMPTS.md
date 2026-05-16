# EcoLink — AI Prompt Rules & Constraints

This file documents the prompt engineering rules for all Gemini calls in `gemini_engine.py`.
**All team members modifying prompts must follow these rules.**

---

## Architecture Overview

EcoLink uses a **Hybrid AI Matching Engine**. Gemini is NOT the only matching layer.

```
Step 2  → Rule-based filter (Python)       matching_engine.py
Step 4  → Weighted formula score (Python)  matching_engine.py
Step 5  → Graph relationship boost (Python) matching_engine.py
Step 6  → Greedy capacity check (Python)   matching_engine.py
Step 7  → Gemini: ground explanation       gemini_engine.py  ← you are here
Step 8  → Human admin approval             app.py
```

Gemini's role is to **explain** pre-scored matches and **flag risks** — not to invent scores.

---

## Global Rules (apply to ALL prompts)

| # | Rule | Why |
|---|------|-----|
| 1 | Always pass real actor profiles from the database | Prevents hallucination — Gemini can only reason about data it receives |
| 2 | Never ask Gemini to invent credentials, history, or facts not in the profile | Core anti-hallucination constraint |
| 3 | Always require strict JSON output schema | Free-form output cannot be parsed reliably |
| 4 | Always include `confidence` (high / medium / low) | Lets admin know when to scrutinise a result |
| 5 | Return ONLY the JSON — no preamble, no explanation outside the schema | Prevents parse failures |
| 6 | Cap output to `top_n` results, ranked by score descending | Prevents bloated responses |

---

## `find_matches()` — Step 7 Rules

**Hybrid mode** (score_breakdowns provided):

| # | Rule |
|---|------|
| 1 | Accept the Formula Match Score exactly as given — copy it into "score", do NOT change it |
| 2 | Explain WHY the match is valuable using ONLY data from the actor profiles |
| 3 | Include exactly one `risk_note` — a specific gap or concern visible in the profiles |
| 4 | Set confidence based on score threshold: high ≥ 0.65, medium 0.35–0.64, low < 0.35 |
| 5 | Set `bias_flag: true` if one candidate dominates the shortlist |

**Fallback mode** (no score_breakdowns — pure LLM):

Same rules as above, except rule 1 — Gemini assigns the score itself (0.0–1.0).

---

## `explain_linkage()` Rules

| # | Rule |
|---|------|
| 1 | Explain in 3–4 sentences only — value created, linkage health, next action |
| 2 | Base health assessment on the engagement history provided — not assumptions |
| 3 | Do not use bullet points |
| 4 | Be practical and actionable — not generic or promotional |

---

## `predict_linkage_success()` Rules

| # | Rule |
|---|------|
| 1 | Base prediction on similar historical engagements provided — not hypotheticals |
| 2 | If no historical data: state clearly that prediction is based on profile compatibility only |
| 3 | Always include `risk_factors[]` and `recommendations[]` |
| 4 | `probability` must be a float 0.0–1.0 |
| 5 | `confidence` must be high / medium / low |

---

## `analyze_ecosystem_health()` Rules

| # | Rule |
|---|------|
| 1 | Base all analysis on the ecosystem snapshot provided (actor counts, industries, ratings) |
| 2 | `health_score` must be integer 0–100 |
| 3 | `status` must be one of: Healthy / Growing / At Risk / Critical |
| 4 | `alert` should be null if there is no urgent issue |

---

## What Gemini Must NEVER Do

- Invent a mentor's credential or publication not in the profile
- Fabricate a past successful match that isn't in the engagement history
- Change a pre-computed formula score
- Return partial JSON or JSON wrapped in markdown (use `_clean_json()` defensively)
- Recommend a candidate that was filtered out by Step 2 (Gemini only sees pre-filtered candidates)

---

## Output Schema Reference

### `find_matches` output item
```json
{
  "actor_id": 3,
  "name": "Dr. Aisha Rahman",
  "score": 0.72,
  "reason": "Dr. Aisha's deep FinTech expertise aligns directly with PayEase's fundraising needs. Her track record mentoring early-stage companies in Kuala Lumpur strengthens the geographic fit.",
  "risk_note": "Dr. Aisha currently holds 3 active mentorships — monitor capacity before committing.",
  "confidence": "high",
  "bias_flag": false
}
```

### `predict_linkage_success` output
```json
{
  "probability": 0.78,
  "confidence": "medium",
  "risk_factors": ["Limited shared history in the AgriTech space"],
  "recommendations": ["Set a 60-day check-in milestone", "Define clear success KPIs upfront"],
  "summary": "Strong profile alignment suggests a likely successful engagement pending clear goals."
}
```

### `analyze_ecosystem_health` output
```json
{
  "health_score": 62,
  "status": "Growing",
  "strengths": ["Diverse industry coverage", "High mentor-to-company ratio"],
  "gaps": ["No GreenTech mentors", "Low engagement rating in FinTech linkages"],
  "top_recommendation": "Recruit 2 GreenTech mentors to serve 3 unmatched companies.",
  "alert": null
}
```

---

## Score Breakdown Reference (Step 4 — matching_engine.py)

| Dimension | Weight | Source |
|-----------|--------|--------|
| Industry Match | 20% | `actor.industry` text overlap |
| Needs / Expertise | 25% | `actor.skills` set intersection |
| Stage / Context | 15% | Description keyword detection |
| Semantic Similarity | 15% | Token overlap across description + industry + skills (MVP proxy for vector embedding) |
| Availability / Capacity | 10% | Active linkage count vs. max capacity (default 5) |
| Historical Feedback | 10% | Bayesian adjusted rating from `engagements` table |
| Programme / Geography | 5% | `actor.location` match |

Graph boost (Step 5) adds 0–10% on top of the formula score for candidates with proven
successful history with similar actors.
