from .base import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class ChatsMessage(Base):
    __tablename__ = "chat_messages"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
    )

    text: Mapped[str]
    author: Mapped[str]
    initials: Mapped[str]
    time: Mapped[str]
