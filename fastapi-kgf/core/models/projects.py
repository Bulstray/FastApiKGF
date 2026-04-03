from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )

    tasks: Mapped["Task"] = relationship(
        "Task",
        back_populates="project",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
