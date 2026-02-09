from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.types import UserRole

from .base import Base
from .mixin import IdIntPkMixin


class User(Base, IdIntPkMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
