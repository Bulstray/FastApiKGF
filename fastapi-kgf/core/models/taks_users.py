from sqlalchemy import ForeignKey

from .base import Base

from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .task import Task


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
