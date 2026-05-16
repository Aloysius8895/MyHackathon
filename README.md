# EcoLink — AI-Powered Ecosystem Relationship Engine

> Build With AI 2026 KL | MyHack | Cradle Fund Challenge

## Problem
Cradle manages Malaysia's innovation ecosystem manually — mentor matching, company allocation, and partner coordination all done by hand. No memory. No reuse. Every cycle starts from zero.

## Solution
EcoLink treats ecosystem relationships as **first-class entities** managed by AI.

- **AI Matching** — Gemini 2.0 Flash ranks mentor↔company pairs with scores, reasons, and confidence levels
- **Living History** — every engagement outcome feeds back into the next matching cycle (flywheel effect)
- **Ethical AI** — confidence scores, bias flags, and human approval before any linkage is created

## Tech Stack
| Layer | Tool |
|-------|------|
| AI Engine | Gemini 2.0 Flash (Google) |
| Frontend | Streamlit |
| Database | SQLite |

## Quick Start
```bash
pip install -r requirements.txt
python seed_data.py
streamlit run app.py
```

## Scalability & Cost Model
| Layer | Current (Demo) | Production |
|-------|---------------|------------|
| Database | SQLite (local) | PostgreSQL on Cloud SQL (~RM50/month) |
| Backend | Local Python | Google Cloud Run (pay-per-request, ~RM0.004/call) |
| AI Engine | Gemini 2.0 Flash | Same — Flash tier keeps cost low at scale |
| Storage | Local filesystem | Google Cloud Storage for exports/reports |

**Cost at scale:**
- 50 programmes/year × 100 matches each = 5,000 Gemini calls/year
- Estimated AI cost: ~USD 2–5/year (Flash pricing)
- Total infra cost at MVP scale: < RM200/month

**Flywheel economics:** more data → better matches → less manual correction → lower operational cost per programme cycle.

## Deployment
Deployable on **Google Cloud Run** with a managed PostgreSQL backend (swap SQLite in `database.py`). Containerisable via Docker in under 30 minutes.

## Stakeholders & Beneficiaries
| Stakeholder | Role | Benefit |
|-------------|------|---------|
| Cradle Programme Managers | Primary users | Eliminate manual coordination, get AI-ranked matches instantly |
| Mentors | Ecosystem actors | Matched to companies that fit their expertise, not random assignment |
| Startups / Companies | Ecosystem actors | Access mentors with proven track records in their domain |
| Government / MDEC | Oversight | Data-driven evidence of ecosystem health and ROI per programme |
| Future Programmes | Beneficiaries | Inherit institutional knowledge from all past cycles (flywheel) |

## Why Gemini 2.0 Flash
| Criteria | Reason |
|----------|--------|
| **Reasoning quality** | Complex multi-actor matching requires contextual understanding, not keyword search — Gemini excels at this |
| **Structured output** | Reliably returns valid JSON with scores, reasons, confidence — critical for a production system |
| **Speed** | Flash variant gives near-instant responses, essential for live demo and real-time UX |
| **Google ecosystem** | Native integration with Google Cloud Run for deployment; aligns with hackathon's Google Tech requirement |
| **Cost efficiency** | Flash tier is cost-effective for high-frequency matching calls in a SaaS model |

## Hallucination Mitigation
| Method | Implementation |
|--------|---------------|
| **Structured JSON prompts** | Every Gemini call demands a strict JSON schema — free-form hallucination is structurally blocked |
| **Confidence scores** | AI self-reports `high / medium / low` confidence; low-confidence matches are visually flagged |
| **Bias flags** | AI detects when one actor dominates recommendations and warns the user |
| **Human-in-the-loop** | No linkage is created automatically — a human must click "Create Linkage" to confirm |
| **Grounded in real data** | All prompts include actual actor profiles from the database, not abstract hypotheticals |
| **Explainability** | Every match includes a written reason — users can verify AI logic before acting |

## AI Ethics
- Confidence scores on every AI recommendation
- Bias flags when one actor dominates matches
- Human-in-the-loop: all linkages require manual approval
- Full reasoning transparency — every match includes an explanation
- Privacy: no personal data sent to Gemini beyond professional profiles

## Team
| Person | Role |
|--------|------|
| Aloysius | Frontend (app.py) |
| P2 | DB + Matching (database.py) |
| Hing | Structure + Embedding |
| Edixon | AI Model (gemini_engine.py) |
