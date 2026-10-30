"""Health check route, used to confirm the API is up and reachable."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health")
def read_health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Report that the API is running and which environment it is running in."""
    return HealthResponse(status="ok", environment=settings.environment)
