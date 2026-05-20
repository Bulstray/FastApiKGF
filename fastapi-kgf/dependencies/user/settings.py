from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services import UserSettingsService


class UserSettingsServiceFactory(UserSettingsService):
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    ) -> None:
        super().__init__(session)

    @classmethod
    def init_user_settings_factory(
        cls,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ):
        return cls(session)
