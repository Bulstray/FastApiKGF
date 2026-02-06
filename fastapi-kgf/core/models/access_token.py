from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

from core.types import UserIdType
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base


class AccessToken(SQLAlchemyBaseAccessTokenTable[UserIdType], Base):
    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyAccessTokenDatabase(session, cls)
