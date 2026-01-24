from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    user: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]
