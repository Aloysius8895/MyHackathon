"""Seed demo profiles into Firebase Firestore.

Usage:
    python scripts/seed_firebase.py

Requires STORAGE_BACKEND=firestore and valid Firebase credentials in .env.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.models import NormalizedProfile, ProfileType
from app.repositories import FirestoreRepository
from app.scoring import text_embedding


DEMO_PROFILES: list[NormalizedProfile] = [
    # --- Companies ---
    NormalizedProfile(
        profile_id="cmp_novaai",
        profile_type=ProfileType.company,
        display_name="NovaAI Finance",
        industry=["FinTech", "SaaS"],
        stage="Seed",
        needs=["Fundraising", "Go-to-market"],
        country="Malaysia",
        verified=True,
        tags=["fintech", "fundraising", "seed", "saas"],
        embedding=text_embedding(["fintech seed fundraising saas payments malaysia"]),
    ),
    NormalizedProfile(
        profile_id="cmp_greenloop",
        profile_type=ProfileType.company,
        display_name="GreenLoop Technologies",
        industry=["Climate", "Manufacturing"],
        stage="MVP",
        needs=["Technical architecture", "Partnerships"],
        country="Malaysia",
        verified=True,
        tags=["climate", "manufacturing", "mvp", "iot"],
        embedding=text_embedding(["climate sustainability manufacturing iot partnerships malaysia"]),
    ),
    NormalizedProfile(
        profile_id="cmp_healthbridge",
        profile_type=ProfileType.company,
        display_name="HealthBridge",
        industry=["HealthTech"],
        stage="Pre-seed",
        needs=["Product strategy", "Go-to-market"],
        country="Singapore",
        verified=True,
        tags=["health", "product", "pre-seed"],
        embedding=text_embedding(["healthtech medical product roadmap go to market singapore"]),
    ),
    # --- Mentors ---
    NormalizedProfile(
        profile_id="men_alina",
        profile_type=ProfileType.mentor,
        display_name="Alina Tan",
        industry=["FinTech"],
        stage="Seed",
        expertise=["Fundraising", "Venture capital", "Go-to-market"],
        country="Malaysia",
        availability=True,
        capacity=3,
        active_assignments=1,
        past_experience=["Mentored seed-stage fintech founders", "Former VC principal"],
        verified=True,
        tags=["fintech", "fundraising", "seed"],
        embedding=text_embedding(["fintech venture capital seed fundraising go to market malaysia"]),
        metadata={"historical_feedback": 4.7},
    ),
    NormalizedProfile(
        profile_id="men_david",
        profile_type=ProfileType.mentor,
        display_name="David Lim",
        industry=["Manufacturing", "IoT"],
        expertise=["Technical architecture", "Supply chain"],
        country="Singapore",
        availability=True,
        capacity=2,
        active_assignments=0,
        past_experience=["Built industrial IoT systems", "Supply chain advisor at Fortune 500"],
        verified=True,
        tags=["manufacturing", "iot", "technical"],
        embedding=text_embedding(["manufacturing industrial iot technical architecture supply chain"]),
        metadata={"historical_feedback": 4.2},
    ),
    NormalizedProfile(
        profile_id="men_lina",
        profile_type=ProfileType.mentor,
        display_name="Lina Gomez",
        industry=["FinTech", "HealthTech"],
        expertise=["Product strategy", "Go-to-market"],
        country="Malaysia",
        availability=False,
        capacity=2,
        active_assignments=2,
        verified=True,
        tags=["fintech", "health", "product"],
        embedding=text_embedding(["fintech healthtech product roadmap go to market malaysia"]),
        metadata={"historical_feedback": 4.8},
    ),
    NormalizedProfile(
        profile_id="men_raj",
        profile_type=ProfileType.mentor,
        display_name="Raj Krishnan",
        industry=["Climate", "SaaS"],
        expertise=["Partnerships", "Technical architecture", "Fundraising"],
        country="Singapore",
        availability=True,
        capacity=4,
        active_assignments=1,
        past_experience=["Co-founded climate tech startup", "Led partnerships at a SaaS unicorn"],
        verified=True,
        tags=["climate", "saas", "partnerships", "fundraising"],
        embedding=text_embedding(["climate sustainability saas partnerships technical fundraising singapore"]),
        metadata={"historical_feedback": 4.5},
    ),
]


async def main() -> None:
    print("Connecting to Firestore...")
    try:
        repo = FirestoreRepository()
    except Exception as exc:
        print(f"Failed to connect: {exc}")
        print("Make sure FIREBASE_PROJECT_ID is set in .env and credentials are configured.")
        sys.exit(1)

    print(f"Seeding {len(DEMO_PROFILES)} profiles...\n")
    for profile in DEMO_PROFILES:
        await repo.save_profile(profile)
        label = "company" if profile.profile_type == ProfileType.company else "mentor"
        print(f"  [{label}] {profile.display_name} ({profile.profile_id})")

    print(f"\nDone. {len(DEMO_PROFILES)} profiles seeded into Firestore.")


if __name__ == "__main__":
    asyncio.run(main())
