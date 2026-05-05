from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types import UserRole

from .base import Base

if TYPE_CHECKING:
    from .message import Message
    from .taks_users import TaskUsers
    from .task import Task


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        unique=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    surname: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.user,
        nullable=False,
        server_default=UserRole.user,
    )

    send_email_tender: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )

    creator_user: Mapped["Task"] = relationship(
        "Task",
        backref="created_by",
    )

    executors_user: Mapped[list["TaskUsers"]] = relationship(
        "TaskUsers",
        back_populates="user_executors",
    )

    user_message: Mapped[list["Message"]] = relationship(
        "Message",
        backref="user_message",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @property
    def full_name(self) -> str:
        """Возвращает полное имя пользователя"""
        return f"{self.name} {self.surname}".strip()

    @property
    def initials(self) -> str:
        return f"{self.name[0]}{self.surname[0]}".upper()
