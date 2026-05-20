from storage.db.crud_user_settings import UserSettingsStorage
from core.schemas import UserSettings
from core.models import UserSettings as UserSettingsModel

from sqlalchemy.ext.asyncio import AsyncSession


class UserSettingsService(UserSettingsStorage):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def update_settings_service(self, user_id: int, settings_form_data):
        settings_schema = UserSettings.model_validate(settings_form_data)

        user_settings = await self.get_by_id(user_id)

        if user_settings:
            await self.update_settings(
                user_id,
                settings_schema,
            )
        else:
            user_settings_model = UserSettingsModel(
                user_id=user_id,
                **settings_schema.model_dump(),
            )
            await self.create(user_settings_model)
