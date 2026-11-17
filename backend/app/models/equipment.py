"""The Equipment model: the kinds of equipment an exercise can need."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Equipment(Base):
    """A kind of equipment an exercise needs, such as a dumbbell or a barbell."""

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
