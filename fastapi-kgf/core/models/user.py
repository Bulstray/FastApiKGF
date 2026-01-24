from sqlalchemy.orm import Mapped, validates, mapped_column

import bcrypt

from .base import Base
from ..enums import UserRole


class User(Base):
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default=UserRole.USER)

    @validates("password")
    def hash_password(self, key, password):
        if password and not password.startswith("$2b$"):
            password_bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password_bytes, salt).decode("utf-8")
        return password
