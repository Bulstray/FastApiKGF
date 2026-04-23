from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from storage.db.crud_user import get_all_users as crud_get_all_users


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> list[User]:
        return await crud_get_all_users(session=self.session)
