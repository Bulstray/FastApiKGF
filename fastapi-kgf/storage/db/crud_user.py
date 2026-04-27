from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from .base_crud import BaseCRUD


class UserStorage(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_user_by_username(self, username: str):
        stmt = select(User).where(username == User.username)
        result = await self.session.scalars(stmt)
        return result.first()
