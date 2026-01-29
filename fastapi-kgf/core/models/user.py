from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from core.enums import UserRole

from .base import Base


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    password: Mapped[bytes] = mapped_column(
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
    )
