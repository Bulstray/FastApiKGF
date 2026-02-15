from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types import UserRole

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .tasks import Tasks


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.user,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)

    tasks_user: Mapped[list["Tasks"]] = relationship(back_populates="executor")
