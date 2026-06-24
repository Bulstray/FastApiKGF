from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User

from .base_crud import BaseCRUD
from core.config.superuser import SuperUserConfig


async def get_all_users(
    session: AsyncSession,
) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    stmt = select(User).where(email == User.email)
    result = await session.scalars(stmt)
    return result.first()


async def update_data_user(
    session: AsyncSession,
    user_in: dict[str, str],
    user_id: int,
) -> None:
    stmt = update(User).where(User.id == user_id).values(**user_in)
    await session.execute(stmt)
    await session.commit()


async def create_user(
    session: AsyncSession,
    user_in: SuperUserConfig,
) -> None:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()


class UserStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def update_data_user(
        self,
        user_in: dict[str, str],
        user_id: int,
    ) -> None:
        stmt = update(User).where(User.id == user_id).values(**user_in)
        await self.session.execute(stmt)
        await self.session.commit()
