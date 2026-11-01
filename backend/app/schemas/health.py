"""Response schema for the health check route."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """What ``GET /api/health`` returns."""

    status: Literal["ok"]
    environment: str
