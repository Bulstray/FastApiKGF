from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserSettings
from core.schemas import UserSettings as UserSchemaSchema

from .base_crud import BaseCRUD
from core.schemas import UserSettings as UserSettingsSchema
from core.models import UserSettings as UserSettingsModel


async def get_settings_by_user(
    session: AsyncSession,
    user_id: int,
) -> UserSettings | None:
    stmt = select(UserSettings).where(UserSettings.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_settings(
    session: AsyncSession,
    user_id: int,
    user_settings: UserSchemaSchema,
) -> None:
    stmt = (
        update(UserSettings)
        .where(UserSettings.user_id == user_id)
        .values(**user_settings.model_dump())
    )

    await session.execute(stmt)
    await session.commit()


async def create_user_settings(
    session: AsyncSession,
    user_id: int,
    user_settings: UserSettingsSchema,
) -> None:
    user_settings = UserSettingsModel(
        user_id=user_id,
        **user_settings.model_dump(),
    )
    session.add(user_settings)
    await session.commit()
    await session.refresh(user_settings)


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
