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

## Deployment
Deployable on **Google Cloud Run** with a managed PostgreSQL backend (swap SQLite in `database.py`). Containerisable via Docker in under 30 minutes.

## AI Ethics
- Confidence scores on every AI recommendation
- Bias flags when one actor dominates matches
- Human-in-the-loop: all linkages require manual approval
- Full reasoning transparency — every match includes an explanation

## Team
| Person | Role |
|--------|------|
| Aloysius | Frontend (app.py) |
| P2 | DB + Matching (database.py) |
| Hing | Structure + Embedding |
| Edixon | AI Model (gemini_engine.py) |
