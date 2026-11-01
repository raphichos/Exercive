"""Application entry point: builds the FastAPI app and registers its routers.

Uvicorn, the web server, loads the ``app`` object defined at the bottom of this file.
"""

from fastapi import FastAPI

from app.config import get_settings
from app.routers import health


def create_app() -> FastAPI:
    """Build and configure the FastAPI application.

    Every route, including the interactive docs, lives under ``/api``. The frontend
    proxies that one prefix to this server, which is what lets the browser treat the
    frontend and backend as a single origin (see docs/ARCHITECTURE.md).
    """
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
    )
    app.include_router(health.router, prefix="/api")
    return app


app = create_app()
