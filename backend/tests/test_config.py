"""Tests for loading settings from environment variables."""

import pytest
from pydantic import ValidationError

from app.config import Settings


def test_environment_is_read_from_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """An ENVIRONMENT variable overrides the default."""
    monkeypatch.setenv("ENVIRONMENT", "production")

    assert Settings(_env_file=None).environment == "production"


def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """A typo in configuration fails loudly at startup rather than being accepted."""
    monkeypatch.setenv("ENVIRONMENT", "prod")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
