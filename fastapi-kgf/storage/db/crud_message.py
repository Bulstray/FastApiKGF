from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ChatsMessage


async def create_chats_message(session: AsyncSession, message: ChatsMessage):
    session.add(message)
    await session.commit()
    await session.refresh(message)
