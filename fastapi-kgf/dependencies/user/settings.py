from sqlalchemy.ext.asyncio import AsyncSession

from services import UserSettingsService
from fastapi import Depends

from typing import Annotated
from core.models import db_helper


class UserSettingsServiceFactory(UserSettingsService):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ) -> None:
        super().__init__(session)
