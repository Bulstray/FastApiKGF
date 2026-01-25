from collections.abc import Sequence

from sqlalchemy import Row, select, delete
from sqlalchemy.orm import Session

from core.models.user import User
from core.schemas import UserCreate
from .user_exceptions import UserAlreadyExists


def get_all_users(
    session: Session,
) -> Sequence[Row[tuple[str, str]]] | None:
    stmt = select(User.username, User.role).order_by(User.id)
    result = session.execute(stmt)
    return result.all()


def get_user_by_username(
    session: Session,
    username: str,
):
    stmt = select(User).where(User.username == username)
    result = session.execute(stmt)
    return result.first()


def check_user_exist(
    session: Session,
    username: str,
):
    stmt = select(User).where(User.username == username)
    result = session.scalar(stmt)
    return result


def create_user(
    session: Session,
    user_in: UserCreate,
) -> User | None:
    user = User(**user_in.model_dump())

    if (
        user_in.role == "admin"
        and check_user_exist(session, user_in.username) is not None
    ):
        return None

    elif check_user_exist(session, user.username) is not None:
        raise UserAlreadyExists(user_in.username)

    session.add(user)
    session.commit()

    return user


def delete_user(
    session: Session,
    username: str,
) -> None:
    stmt = delete(User).where(User.username == username)
    session.execute(stmt)
    session.commit()
