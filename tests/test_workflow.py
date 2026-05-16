from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.repositories import InMemoryRepository


def build_client() -> TestClient:
    app = create_app(
        repository=InMemoryRepository(seed_demo_data=False),
        settings=Settings(auth_mode="disabled", storage_backend="memory", ai_provider="heuristic"),
    )
    return TestClient(app)


def test_uploaded_files_run_full_matching_workflow() -> None:
    client = build_client()

    response = client.post(
        "/workflow/run",
        data={"limit": "3"},
        files=[
            (
                "company_files",
                (
                    "nova-pay.txt",
                    (
                        "NovaPay is a Malaysia FinTech SaaS startup at seed stage. "
                        "It needs fundraising and go-to-market support for SME payments."
                    ),
                    "text/plain",
                ),
            ),
            (
                "mentor_files",
                (
                    "alina-tan.txt",
                    (
                        "Alina Tan is a Malaysia FinTech mentor and former VC principal. "
                        "She is available for 3 active mentees and helps with fundraising and go-to-market."
                    ),
                    "text/plain",
                ),
            ),
        ],
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["ingested"]) == 2
    assert payload["ingested"][0]["vectorDimensions"] == 32
    assert payload["matches"][0]["recommendations"][0]["mentor_id"] == "men_alina_tan"
    assert payload["report"]


def test_history_upload_persists_dataset_with_mentor_name() -> None:
    client = build_client()
    payload = {
        "companies": [{"id": "co_001", "name": "AutoTech"}],
        "mentors": [{"id": "me_001", "name": "Aloysius Lee"}],
        "engagements": [
            {
                "mentor_id": "me_001",
                "mentor_name": "Aloysius Lee",
                "company": "AutoTech",
                "outcome": "Prototype review",
                "score": 0.9,
            }
        ],
    }

    response = client.post("/history/upload", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "saved"
    assert response.json()["mentors"] == 1

    saved = client.get("/history/sessions")
    assert saved.status_code == 200
    data = saved.json()
    assert data["companies"][0]["name"] == "AutoTech"
    assert data["mentors"][0]["name"] == "Aloysius Lee"
    assert data["engagements"][0]["mentor_name"] == "Aloysius Lee"
    assert data["uploadedAt"]


def test_history_upload_accumulates_people_and_sessions() -> None:
    client = build_client()

    first = {
        "mentors": [{"id": "me_001", "name": "Ahmad Farid bin Razak"}],
        "engagements": [{"session_id": "SES-1001", "mentor_id": "me_001", "company": "CloudNine", "outcome": "AI planning", "score": 4.8}],
    }
    second = {
        "mentors": [{"id": "me_002", "name": "Priya Ramasamy"}],
        "engagements": [{"session_id": "SES-1002", "mentor_name": "Priya Ramasamy", "company": "DataSpark", "outcome": "Analytics review", "score": 4.7}],
    }

    assert client.post("/history/upload", json=first).status_code == 200
    assert client.post("/history/upload", json=second).status_code == 200

    data = client.get("/history/sessions").json()
    mentor_names = {mentor["name"] for mentor in data["mentors"]}
    session_names = {engagement["mentor_name"] for engagement in data["engagements"]}
    assert mentor_names == {"Ahmad Farid bin Razak", "Priya Ramasamy"}
    assert session_names == {"Ahmad Farid bin Razak", "Priya Ramasamy"}
