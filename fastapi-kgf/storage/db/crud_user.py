from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User


async def get_user_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    """Возвращает пользователя по имени"""
    stmt = select(User).where(username == User.username)
    result = await session.scalars(stmt)
    return result.first()


async def create_user(session: AsyncSession, user: User) -> User:
    """Создание пользователя"""
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)
