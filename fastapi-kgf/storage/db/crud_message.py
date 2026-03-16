from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func

from core.models import Message, MessageFile
from core.schemas.message import Message as MessageSchema


async def create_chats_message(
    session: AsyncSession,
    message_in: MessageSchema,
) -> Message:
    message = Message(**message_in.model_dump())
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def create_file_data_message(
    session: AsyncSession,
    file: MessageFile,
) -> MessageFile:
    session.add(file)
    await session.commit()
    await session.refresh(file)
    return file


async def get_message_by_id(
    session: AsyncSession,
    task_id: int,
) -> list[Message]:
    message = (
        select(Message).where(Message.task_id == task_id).order_by(Message.task_id)
    )

    result = await session.scalars(message)
    return list(result.all())


async def update_mark_read_message(
    session: AsyncSession,
    task_id: int,
):
    message = update(Message).where(Message.task_id == task_id).values(is_read=True)
    await session.execute(message)
    await session.commit()


async def count_unread_messages(
    session: AsyncSession,
):
    stmt = select(Message.task_id, func.count(Message.id)).where(
        Message.is_read == False
    )
    result = await session.execute(stmt)

    counts = {task_id: count for task_id, count in result.all()}
    return counts
