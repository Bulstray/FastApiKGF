import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, validates

from core.enums import UserRole

from .base import Base


class User(Base):
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default=UserRole.USER)

    @validates("password")
    def hash_password(self, key: str, password: str) -> bytes | str:
        if password and not password.startswith("$2b$"):
            password_bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password_bytes, salt)
        return password
