# Hybrid AI Relationship Matching Engine

FastAPI backend for automating ecosystem linkages instead of manual coordination.

The MVP focuses on **Company-to-Mentor matching**. It treats recommendations, approvals, relationships, and feedback as reusable backend entities that a separate frontend can consume through REST APIs.

## What It Does

- Extracts structured profile data from messy company and mentor descriptions.
- Filters invalid matches with deterministic eligibility rules.
- Retrieves mentor candidates using tags plus semantic similarity.
- Scores matches with a transparent weighted formula.
- Adds graph-lite relationship signals from needs, expertise, tags, and past experience.
- Stores recommendations in an admin approval queue.
- Creates relationship entities only after admin approval.
- Collects feedback and applies Bayesian averaging for future learning.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | FastAPI, Pydantic v2 |
| Database | Firebase Firestore adapter, in-memory demo mode |
| Auth | Firebase Auth token validation, disabled local mode |
| AI | Gemini / Vertex AI-ready extraction and explanation boundary |
| Vector Search | Embedding fields with local cosine fallback; Firestore Vector Search-ready storage |
| Deployment | Google Cloud Run, Docker |
| Frontend | Not included; handled by another teammate |

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

The default `.env.example` uses `STORAGE_BACKEND=memory` and `AUTH_MODE=disabled`, so the backend runs without Firebase credentials.

## API Endpoints

- `POST /profiles/extract/company`
- `POST /profiles/extract/mentor`
- `GET /profiles/extract/{actorType}/{actorId}`
- `POST /profiles/extract`
- `POST /matches/run`
- `GET /recommendations`
- `POST /recommendations/{id}/approve`
- `POST /recommendations/{id}/reject`
- `POST /recommendations/{id}/override`
- `GET /relationships`
- `POST /relationships/{id}/feedback`
- `GET /health`

## Demo Request

Extract a company profile:

```bash
curl -X POST http://127.0.0.1:8000/profiles/extract/company ^
  -H "Content-Type: application/json" ^
  -d "{\"companyId\":\"cmp_novapay\",\"displayName\":\"NovaPay\",\"rawProfileText\":\"NovaPay is a Malaysia FinTech SaaS startup at seed stage. It needs fundraising and go-to-market support.\"}"
```

Run matching:

```bash
curl -X POST http://127.0.0.1:8000/matches/run ^
  -H "Content-Type: application/json" ^
  -d "{\"company_id\":\"cmp_novaai\",\"limit\":3}"
```

The in-memory demo repository includes one verified FinTech company and several mentors with different eligibility, capacity, expertise, and availability signals.

## Firestore Mode

Set these environment variables for Cloud Run or local Firebase testing:

```text
STORAGE_BACKEND=firestore
AUTH_MODE=firebase
GOOGLE_APPLICATION_CREDENTIALS=path\to\service-account.json
FIREBASE_PROJECT_ID=your-project-id
```

Do not commit real `.env` files or service account keys.

## Gemini / Vertex AI Mode

The default local mode uses deterministic heuristic extraction so tests and demos run without cloud credentials. To use Gemini through Vertex AI, set:

```text
AI_PROVIDER=gemini
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GEMINI_MODEL=gemini-1.5-flash
```

Extraction endpoints store raw profile text, normalized extracted JSON, extraction status, confidence, and extraction logs in Firestore collections: `companies`, `mentors`, and `extraction_logs`.

## Tests

```bash
pytest
```

The tests use in-memory storage and cover matching, approval, relationship creation, feedback learning, and profile extraction.
