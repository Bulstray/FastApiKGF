from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message_file import MessageFile
    from .task import Task


class Message(Base):
    __tablename__ = "messages"

    task_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    author: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    initials: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    created_at: Mapped[str] = mapped_column(
        nullable=False,
    )

    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="messages",
    )

    file: Mapped["MessageFile"] = relationship(
        "MessageFile",
        back_populates="message",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
