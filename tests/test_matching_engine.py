from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.repositories import InMemoryRepository


def build_client() -> TestClient:
    app = create_app(
        repository=InMemoryRepository(seed_demo_data=True),
        settings=Settings(auth_mode="disabled", storage_backend="memory"),
    )
    return TestClient(app)


def test_run_match_returns_ranked_recommendations() -> None:
    client = build_client()

    response = client.post("/matches/run", json={"company_id": "cmp_novaai", "limit": 3})

    assert response.status_code == 200
    payload = response.json()
    assert payload["company_id"] == "cmp_novaai"
    assert payload["recommendations"]
    assert payload["recommendations"][0]["mentor_id"] == "men_alina"
    assert payload["recommendations"][0]["match_score"] > 70
    assert payload["recommendations"][0]["status"] == "pending"


def test_approve_recommendation_creates_relationship() -> None:
    client = build_client()
    recommendation = client.post("/matches/run", json={"company_id": "cmp_novaai", "limit": 1}).json()["recommendations"][0]

    response = client.post(
        f"/recommendations/{recommendation['recommendation_id']}/approve",
        json={"admin_id": "admin_1", "note": "Looks good"},
    )

    assert response.status_code == 200
    relationship = response.json()
    assert relationship["company_id"] == "cmp_novaai"
    assert relationship["mentor_id"] == "men_alina"
    assert relationship["approved_by_admin"] == "admin_1"

    recommendations = client.get("/recommendations", params={"status": "accepted"}).json()
    assert recommendations[0]["recommendation_id"] == recommendation["recommendation_id"]


def test_feedback_updates_bayesian_score_and_outcome() -> None:
    client = build_client()
    recommendation = client.post("/matches/run", json={"company_id": "cmp_novaai", "limit": 1}).json()["recommendations"][0]
    relationship = client.post(
        f"/recommendations/{recommendation['recommendation_id']}/approve",
        json={"admin_id": "admin_1"},
    ).json()

    response = client.post(
        f"/relationships/{relationship['relationship_id']}/feedback",
        json={"source_id": "cmp_novaai", "source_role": "company", "rating": 5, "outcome": "completed_successfully"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["status"] == "completed"
    assert updated["feedback_score"] == 3.88
    assert updated["outcome"] == "completed_successfully"


def test_profile_extraction_saves_normalized_profile() -> None:
    client = build_client()

    response = client.post(
        "/profiles/extract",
        json={
            "profile_type": "mentor",
            "display_name": "Maya VC",
            "raw_text": "Maya is a Malaysia FinTech mentor with venture capital fundraising and seed investment experience.",
            "metadata": {"capacity": 2, "verified": True},
        },
    )

    assert response.status_code == 201
    profile = response.json()
    assert profile["display_name"] == "Maya VC"
    assert "FinTech" in profile["industry"]
    assert "Fundraising" in profile["expertise"]
    assert profile["country"] == "Malaysia"
