import bcrypt
from sqlalchemy.orm import Session

from core.models import User
from crud import user as user_crud


def authenticate_user(
    session: Session,
    username: str,
    password: str,
) -> User | None:
    user = user_crud.get_user_by_username(
        session=session,
        username=username,
    )
    if not user:
        return None

    if not bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=user.password,
    ):
        return None

    return user
