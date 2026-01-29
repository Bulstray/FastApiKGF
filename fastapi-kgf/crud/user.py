from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from core.models.user import User


def get_all_users(
    session: Session,
) -> list[User]:
    """Возвращает всех пользователей как объект User"""
    stmt = select(User).order_by(User.id)
    return list(session.scalars(stmt).all())


def get_user_by_username(
    session: Session,
    username: str,
) -> User | None:
    """Возвращает пользователя по username"""
    stmt = select(User).where(User.username == username)
    return session.scalars(stmt).first()


def create_user(
    session: Session,
    user: User,
) -> User:
    """Создает пользователя в БД"""
    session.add(user)
    session.commit()
    return user


def delete_user(
    session: Session,
    username: str,
) -> None:
    """Удаляет пользователя"""
    stmt = delete(User).where(User.username == username)
    session.execute(stmt)
    session.commit()
