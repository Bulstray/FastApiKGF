import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String, Text, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.tasks import TaskStatus

from ..schemas.tasks import Task
from .base import Base

if TYPE_CHECKING:
    from .message import Message
    from .message_read_status import MessageReadStatus
    from .taks_users import TaskUsers


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

    deadline: Mapped[datetime] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
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

    task_users: Mapped[list["TaskUsers"]] = relationship(
        "TaskUsers",
        back_populates="executors",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        cascade="all, delete-orphan",
    )

    read_status: Mapped["MessageReadStatus"] = relationship(
        "MessageReadStatus",
        cascade="all, delete-orphan",
    )


@event.listens_for(Task, "after_delete")
def delete_file_after_delete(mapper, connection, target):
    folder_file = Path(target.folder_file)
    if folder_file.exists():
        folder_file.unlink()
