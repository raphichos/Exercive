"""The Exercise model: one movement in the library, like bench press or cable fly."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Exercise(Base):
    """A specific type of exercise conducted in a workout."""

    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
    is_compound: Mapped[bool] = mapped_column()
    is_main_lift: Mapped[bool] = mapped_column(default=False)
