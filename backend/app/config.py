"""Application settings, read from environment variables and backend/.env.

Keeping configuration here means secrets never appear in code, and the same code
can run locally and in production with different values.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Typed application settings; a wrong value fails at startup, not mid-request."""

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    app_name: str = "Exercive API"
    environment: Literal["development", "test", "production"] = "development"


@lru_cache
def get_settings() -> Settings:
    """Return the shared settings object, so .env is only read once per process."""
    return Settings()
