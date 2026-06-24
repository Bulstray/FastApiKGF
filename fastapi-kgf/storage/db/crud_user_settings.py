from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserSettings
from core.schemas import UserSettings as UserSchemaSchema

from .base_crud import BaseCRUD


async def get_settings_by_user(
    session: AsyncSession,
    user_id: int,
) -> UserSettings | None:
    stmt = select(UserSettings).where(UserSettings.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


class UserSettingsStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserSettings)

    async def update_settings(
        self,
        user_id: int,
        user_settings: UserSchemaSchema,
    ) -> None:
        stmt = (
            update(UserSettings)
            .where(UserSettings.user_id == user_id)
            .values(**user_settings.model_dump())
        )

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_settings_by_user(self, user_id: int) -> UserSettings | None:
        stmt = select(UserSettings).where(UserSettings.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
