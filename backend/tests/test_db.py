"""Test proving a bad equipment_id gets rejected."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import Base, create_db_engine
from app.models import Exercise


def test_exercise_with_unknown_equipment_is_rejected() -> None:
    """An exercise pointing at equipment that doesn't exist is refused, as PostgreSQL would."""
    engine = create_db_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Exercise(name="bicep curl", equipment_id=999, is_compound=False))

        with pytest.raises(IntegrityError):
            session.commit()
