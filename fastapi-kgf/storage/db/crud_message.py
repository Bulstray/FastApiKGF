from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Message, MessageFile


async def create_chats_message(
    session: AsyncSession,
    message: Message,
):
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def create_file_data_message(
    session: AsyncSession,
    file: MessageFile,
):
    session.add(file)
    await session.commit()
    await session.refresh(file)
    return file
