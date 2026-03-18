from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class TaskUsers(Base):
    __tablename__ = "task_users"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

    executors: Mapped["Task"] = relationship(
        "Task",
        back_populates="task_users",
    )

    user_executors: Mapped["User"] = relationship(
        "User",
        back_populates="executors_user",
        lazy="selectin",
    )
