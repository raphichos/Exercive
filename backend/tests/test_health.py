"""Tests for the health check route, sent through the full FastAPI app."""

from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    """The health route is reachable under /api and reports a healthy status."""
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_reports_configured_environment() -> None:
    """The route reads its environment from settings instead of hardcoding it."""
    app.dependency_overrides[get_settings] = lambda: Settings(environment="test")
    try:
        response = client.get("/api/health")
    finally:
        app.dependency_overrides.clear()

    assert response.json()["environment"] == "test"


def test_routes_outside_api_prefix_do_not_exist() -> None:
    """The frontend proxies only /api, so routes must not be served outside that prefix."""
    assert client.get("/health").status_code == 404
