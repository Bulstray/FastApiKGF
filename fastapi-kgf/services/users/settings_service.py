from fastapi.datastructures import FormData
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserSettings as UserSettingsModel
from core.schemas import UserSettings
from storage.db.crud_user_settings import UserSettingsStorage


class UserSettingsService(UserSettingsStorage):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def update_settings_service(
        self,
        user_id: int,
        settings_form_data: FormData,
    ) -> None:
        settings_schema = UserSettings.model_validate(settings_form_data)

        user_settings = await self.get_settings_by_user(user_id)

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
