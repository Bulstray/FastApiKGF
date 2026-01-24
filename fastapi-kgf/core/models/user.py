from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

from .base import Base

import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    moderator = "moderator"


class User(Base):
    user: Mapped[str]
    password: Mapped[str]
    role: Mapped[str] = mapped_column(Enum(UserRole), default=UserRole.USER,)
