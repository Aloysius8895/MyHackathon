# CLAUDE.md

This repository contains a FastAPI backend for a hackathon Matching Engine.

## Project

The backend exposes REST APIs for company-to-mentor matching, admin approval, relationship creation, and feedback learning. The frontend is handled separately.

## Running

```bash
pip install -r requirements.txt
python main.py
```

API docs are available at `http://127.0.0.1:8000/docs`.

## Testing

```bash
pytest
```

Default local mode uses in-memory demo data and disabled auth. Firestore and Firebase Auth are enabled through environment variables.
