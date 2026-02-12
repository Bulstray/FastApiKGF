import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from storage import crud_user


async def validate_basic_auth_user(
    username: str,
    password: str,
    session: AsyncSession,
) -> User | bool:
    user_in_db = await crud_user.get_user_by_username(
        session=session,
        username=username,
    )

    if user_in_db is None:
        return False

    if not bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=user_in_db.hashed_password.encode("utf-8"),
    ):
        return False

    return user_in_db
