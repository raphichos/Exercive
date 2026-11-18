"""Database connection setup: the engine, the session factory and the model base class.

Everything that talks to the database goes through here, so switching from SQLite (local)
to PostgreSQL (production) only means changing DATABASE_URL, not code.
"""

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import ConnectionPoolEntry

from app.config import get_settings


def _enable_sqlite_foreign_keys(
    dbapi_connection: DBAPIConnection, _connection_record: ConnectionPoolEntry
) -> None:
    """Turn on foreign key checks for a new SQLite connection.

    SQLite ignores foreign keys unless each connection asks for them; PostgreSQL always
    enforces them. Without this, a bad equipment_id would be accepted locally and only
    rejected in production.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_engine(database_url: str) -> Engine:
    """Create an engine for the given URL, with the SQLite fixes applied when needed.

    The app and the tests both build engines through this function, so a test database
    behaves exactly like the real one.
    """
    if not database_url.startswith("sqlite"):
        return create_engine(database_url)

    # SQLite refuses by default to let a connection be used from a different thread than the
    # one that opened it. FastAPI runs sync routes in a thread pool, so we switch that check off.
    sqlite_engine = create_engine(database_url, connect_args={"check_same_thread": False})
    event.listen(sqlite_engine, "connect", _enable_sqlite_foreign_keys)
    return sqlite_engine


engine = create_db_engine(get_settings().database_url)

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
