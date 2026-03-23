from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class MessageReadStatus(Base):
    __tablename__ = "message_read_status"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="read_status",
    )

    count: Mapped[int] = mapped_column(default=0)
