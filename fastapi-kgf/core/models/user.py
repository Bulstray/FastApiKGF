from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types import UserRole

from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
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

    executed_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="executor",
        foreign_keys="[Task.executor_id]",
    )

    created_at: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="customer",
        foreign_keys="[Task.customer_id]",
    )
