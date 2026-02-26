from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from services.files import FilesService
from services.messages.message_service import MessageManager


async def get_message_service(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> MessageManager:
    file_service = FilesService(settings.uploads_file_in_chat)
    return MessageManager(
        session=session,
        file_service=file_service,
    )
