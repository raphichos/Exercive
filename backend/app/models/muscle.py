"""The Muscle model: the muscle groups exercises are linked to."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Muscle(Base):
    """A muscle group that exercises target, such as chest or lats."""

    __tablename__ = "muscles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
