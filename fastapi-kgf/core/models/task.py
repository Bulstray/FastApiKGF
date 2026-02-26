from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.tasks import TaskStatus

from .base import Base
from .user import User

if TYPE_CHECKING:
    from .message import Message
    from .user import User


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    deadline: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
    )

    executor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    executor: Mapped["User"] = relationship(
        "User",
        back_populates="executed_tasks",
        foreign_keys=[executor_id],
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    customer: Mapped["User"] = relationship(
        "User",
        back_populates="created_at",
        foreign_keys=[customer_id],
    )

    filename: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    folder_file: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.NOT_STARTED,
        nullable=False,
        server_default=TaskStatus.NOT_STARTED,
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="task",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


@event.listens_for(Task, "after_delete")
def delete_file_after_delete(mapper, connection, target):
    folder_file = Path(target.folder_file)
    if folder_file.exists():
        folder_file.unlink()
