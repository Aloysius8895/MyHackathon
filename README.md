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
| Frontend | Streamlit (`app.py`) + Astro (`part2/`) |
| FastAPI Backend | FastAPI + Pydantic v2 (`app/`) |
| Database | SQLite (demo) / Firebase Firestore (production) |
| Vector Search | Gemini embeddings + cosine similarity |
| Deployment | Google Cloud Run, Docker |

## Quick Start — Streamlit UI
```bash
pip install -r requirements.txt
python seed_data.py
streamlit run app.py
```

## Quick Start — FastAPI Backend
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```
Open API docs: http://127.0.0.1:8000/docs

## API Endpoints
- `POST /profiles/extract/company`
- `POST /profiles/extract/mentor`
- `POST /matches/run`
- `GET /recommendations`
- `POST /recommendations/{id}/approve`
- `POST /recommendations/{id}/reject`
- `POST /relationships/{id}/feedback`
- `GET /health`

## Semantic Matchmaker (Hing)
Node.js + Gemini embeddings + Firestore cosine search:
```bash
cd part2/salo-inspired-frontend
npm install
npm run dev
```
Frontend at http://127.0.0.1:4321

## Stakeholders
| Stakeholder | Benefit |
|-------------|---------|
| Cradle Programme Managers | Eliminate manual coordination, AI-ranked matches instantly |
| Mentors | Matched to companies that fit their expertise |
| Startups | Access mentors with proven track records in their domain |
| Government / MDEC | Data-driven evidence of ecosystem health and ROI |

## Team
| Person | Contribution |
|--------|-------------|
| Aloysius | FastAPI backend (`app/`), app structure, scoring, AI modules |
| Edixon | Streamlit UI (`app.py`), Gemini AI engine, hybrid matching |
| Hing | Node.js semantic matchmaker, Gemini embeddings, Firestore search |
| Lee | Project coordination |
