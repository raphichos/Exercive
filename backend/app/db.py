"""Database connection setup: the engine, the session factory and the model base class.

Everything that talks to the database goes through here, so switching from SQLite (local)
to PostgreSQL (production) only means changing DATABASE_URL, not code.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

# SQLite refuses by default to let a connection be used from a different thread than the one
# that opened it. FastAPI runs sync routes in a thread pool, so we switch that check off.
# PostgreSQL has no such rule, so the argument is only passed for SQLite.
_connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=_connect_args)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Parent class for every model; it collects their tables so Alembic can find them."""


def get_db() -> Iterator[Session]:
    """Give one route a database session and always close it afterwards.

    Used as a FastAPI dependency: `db: Annotated[Session, Depends(get_db)]`.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
