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


def test_extract_company_profile_writes_company_document_and_log() -> None:
    client = build_client()

    response = client.post(
        "/profiles/extract/company",
        json={
            "companyId": "cmp_novapay",
            "displayName": "NovaPay",
            "rawProfileText": (
                "NovaPay is a Malaysia-based FinTech SaaS startup at seed stage. "
                "It helps SMEs automate payments and needs fundraising, go-to-market help, "
                "and bank partnerships across Southeast Asia."
            ),
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["actorType"] == "company"
    assert payload["actorId"] == "cmp_novapay"
    assert payload["extractedProfile"]["companyName"]
    assert "FinTech" in payload["extractedProfile"]["industry"]
    assert "Fundraising" in payload["extractedProfile"]["needs"]
    assert payload["logId"].startswith("log_")

    stored = client.get("/profiles/extract/company/cmp_novapay")
    assert stored.status_code == 200
    assert stored.json()["actorId"] == "cmp_novapay"


def test_extract_mentor_profile_writes_mentor_document() -> None:
    client = build_client()

    response = client.post(
        "/profiles/extract/mentor",
        json={
            "mentorId": "men_alina",
            "displayName": "Alina Tan",
            "rawProfileText": (
                "Alina Tan is a Malaysia FinTech mentor and former VC principal. "
                "She mentored seed-stage startups on fundraising and investor readiness "
                "and is available for 2 active mentees this quarter."
            ),
        },
    )

    assert response.status_code == 201
    profile = response.json()["extractedProfile"]
    assert "FinTech" in profile["industries"]
    assert "Fundraising" in profile["expertise"]
    assert profile["maxCapacity"] == 2


def test_duplicate_company_extraction_requires_force_reextract() -> None:
    client = build_client()
    payload = {
        "companyId": "cmp_duplicate",
        "displayName": "Duplicate Co",
        "rawProfileText": "Duplicate Co is a Malaysia FinTech seed startup needing fundraising support.",
    }

    first = client.post("/profiles/extract/company", json=payload)
    second = client.post("/profiles/extract/company", json=payload)
    forced = client.post("/profiles/extract/company", json={**payload, "forceReextract": True})

    assert first.status_code == 201
    assert second.status_code == 409
    assert forced.status_code == 201
    assert forced.json()["profileVersion"] == 2


def test_missing_raw_profile_text_is_rejected() -> None:
    client = build_client()

    response = client.post(
        "/profiles/extract/company",
        json={"companyId": "cmp_bad", "displayName": "Bad Co", "rawProfileText": ""},
    )

    assert response.status_code == 422


def test_unknown_extracted_profile_returns_404() -> None:
    client = build_client()

    response = client.get("/profiles/extract/company/missing_company")

    assert response.status_code == 404
