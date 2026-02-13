import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from storage.db import crud_user


async def validate_basic_auth_user(
    username: str,
    password: str,
    session: AsyncSession,
) -> User | None:
    user_in_db = await crud_user.get_user_by_username(
        session=session,
        username=username,
    )

    if user_in_db is None:
        return None

    if not bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=user_in_db.hashed_password.encode("utf-8"),
    ):
        return None

    return user_in_db
