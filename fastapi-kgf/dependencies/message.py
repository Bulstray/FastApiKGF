from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.messages.message_service import MessageManager


async def get_message_service(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return MessageManager(session=session)
