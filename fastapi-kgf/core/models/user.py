from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_users.db import SQLAlchemyBaseUserTable

from core.enums import UserRole

from .base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
