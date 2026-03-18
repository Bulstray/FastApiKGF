from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .message_file import MessageFile


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

    author: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[str] = mapped_column(
        nullable=False,
    )

    file: Mapped["MessageFile"] = relationship(
        "MessageFile",
        backref="message",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
