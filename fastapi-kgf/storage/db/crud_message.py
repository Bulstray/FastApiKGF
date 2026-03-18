from sqlalchemy import and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Message, MessageFile, MessageReadStatus
from core.schemas.message import Message as MessageSchema
from core.schemas.message_read_status import (
    MessageReadStatus as MessageReadStatusSchema,
)


async def create_chats_message(
    session: AsyncSession,
    message_in: MessageSchema,
) -> int:
    message = Message(**message_in.model_dump())
    session.add(message)
    await session.flush()
    message_id = message.id
    await session.commit()
    return message_id


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
        select(Message)
        .where(Message.task_id == task_id)
        .order_by(Message.task_id)
        .options(selectinload(Message.user_message))
    )

    result = await session.scalars(message)
    return list(result.all())


async def update_mark_read_message(session: AsyncSession, task_id: int, user_id: int):
    message = (
        update(MessageReadStatus)
        .where(
            and_(
                MessageReadStatus.task_id == task_id,
                MessageReadStatus.user_id == user_id,
            ),
        )
        .values(count=0)
    )
    await session.execute(message)
    await session.commit()


async def count_unread_messages(
    session: AsyncSession,
    user_id: int,
):
    stmt = select(MessageReadStatus.task_id, func.count(MessageReadStatus.id)).where(
        and_(
            MessageReadStatus.is_read == False,
            MessageReadStatus.user_id == user_id,
        ),
    )
    result = await session.execute(stmt)

    counts = {task_id: count for task_id, count in result.all()}
    return counts


async def update_count_unread(
    session: AsyncSession,
    task_id: int,
    users_id: int,
):
    stmt = (
        update(MessageReadStatus)
        .where(
            and_(
                MessageReadStatus.task_id == task_id,
                MessageReadStatus.user_id == users_id,
            ),
        )
        .values(count=MessageReadStatus.count + 1)
    )
    await session.execute(stmt)
    await session.commit()


async def get_unread_message(
    session: AsyncSession,
    user_id: int,
):
    stmt = select(MessageReadStatus.task_id, MessageReadStatus.count).where(
        MessageReadStatus.user_id == user_id,
    )
    result = await session.execute(stmt)
    return {task_message.task_id: task_message.count for task_message in result.all()}


async def add_count_unread_messages(
    session: AsyncSession,
    users_id: MessageReadStatusSchema,
):
    for user_id in users_id.users_id:
        session.add(
            MessageReadStatus(
                user_id=user_id,
                task_id=users_id.task_id,
            ),
        )
    await session.commit()
