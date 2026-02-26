from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.messages.message_service import MessageManager
from services.files import FilesService
from core.config import settings


async def get_message_service(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    file_service = FilesService(settings.uploads_file_in_chat)
    return MessageManager(
        session=session,
        file_service=file_service,
    )
