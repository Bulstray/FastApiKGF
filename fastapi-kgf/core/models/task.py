from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from core.types.tasks import TaskStatus
from sqlalchemy import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import ChatsMessage


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

    chat_messages: Mapped[list["ChatsMessage"]] = relationship(
        "ChatsMessage",
        backref="task",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
