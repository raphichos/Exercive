"""SQLAlchemy models: Python classes that map to database tables.

Every model is imported here so that importing `app.models` registers all tables on
`Base.metadata`. Alembic reads that metadata to generate migrations, so a model missing from
this file is a table Alembic never sees.
"""

from app.models.equipment import Equipment
from app.models.exercise import Exercise
from app.models.muscle import Muscle

__all__ = ["Equipment", "Exercise", "Muscle"]
