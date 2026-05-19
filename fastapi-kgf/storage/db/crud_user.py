from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.schemas import UserUpdate

from .base_crud import BaseCRUD


class UserStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(email == User.email)
        result = await self.session.scalars(stmt)
        return result.first()
