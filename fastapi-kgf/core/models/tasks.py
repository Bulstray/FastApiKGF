from datetime import datetime

from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Tasks(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[str]

    executor: Mapped["User"] = relationship(back_populates="tasks_user")
