from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    app_name: str = "Hybrid AI Relationship Matching Engine"
    environment: str = "local"
    storage_backend: Literal["memory", "firestore"] = "memory"
    auth_mode: Literal["disabled", "firebase"] = "disabled"
    ai_provider: Literal["heuristic", "gemini"] = "heuristic"
    gemini_api_key: str | None = None
    firebase_project_id: str | None = None
    google_cloud_project: str | None = None
    google_cloud_location: str = "us-central1"
    gemini_model: str = "gemini-1.5-flash"
    gemini_temperature: float = Field(default=0.1, ge=0, le=2)
    extraction_confidence_threshold: float = Field(default=0.7, ge=0, le=1)
    max_profile_text_chars: int = Field(default=12000, ge=500, le=100000)
    default_recommendation_limit: int = Field(default=5, ge=1, le=50)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
