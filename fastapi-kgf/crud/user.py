from collections.abc import Sequence

from sqlalchemy import Row, select, delete
from sqlalchemy.orm import Session

from core.models.user import User
from core.schemas import UserCreate


def get_all_users(
    session: Session,
) -> Sequence[Row[tuple[str, str]]] | None:
    stmt = select(User.username, User.role).order_by(User.id)
    result = session.execute(stmt)
    return result.all()


def create_user(
    session: Session,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
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
