from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from services.files import FilesService
from services.messages.message_service import MessageManager


class TaskMessageFactory(MessageManager):
    def __init__(
        self,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
    ) -> None:
        file_service = FilesService(settings.uploads_file_in_chat)
        super().__init__(
            session,
            file_service,
        )
