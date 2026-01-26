import bcrypt
from sqlalchemy.orm import Session

from crud import user as user_crud


def get_user_password(session: Session, username: str):
    return user_crud.get_user_by_username(
        session=session,
        username=username,
    )


def check_password_match(password1: str, password2: str) -> bool:
    hashed_password_bytes = password1
    return bcrypt.checkpw(
        password=password2.encode("utf-8"),
        hashed_password=hashed_password_bytes,
    )
