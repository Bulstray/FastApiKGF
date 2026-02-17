from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from core.types.tasks import TaskStatus
from sqlalchemy import Enum


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(
        unique=True,
    )
    description: Mapped[str]
    deadline: Mapped[str]
    executor: Mapped[str]
    customer: Mapped[str]
    file: Mapped[str | None]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.NOT_STARTED,
    )
