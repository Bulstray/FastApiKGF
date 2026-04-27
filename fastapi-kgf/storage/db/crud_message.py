from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Message, MessageReadStatus

from .base_crud import BaseCRUD


class MessageStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Message)

    async def get_unread_message(self, user_id: int) -> dict[int, int]:
        stmt = select(
            MessageReadStatus.task_id,
            MessageReadStatus.count,
        ).where(MessageReadStatus.user_id == user_id)

        result = await self.session.execute(stmt)
        return {
            task_message.task_id: task_message.count for task_message in result.all()
        }

    async def get_messages_for_task(
        self,
        task_id: int,
    ) -> list[Message]:
        message = (
            select(Message)
            .where(Message.task_id == task_id)
            .order_by(Message.id)
            .options(selectinload(Message.user_message))
        )

        result = await self.session.scalars(message)
        return list(result.all())

    async def update_count_unread(
        self,
        task_id: int,
        user_id: int,
    ) -> None:
        stmt = (
            update(MessageReadStatus)
            .where(
                and_(
                    MessageReadStatus.task_id == task_id,
                    MessageReadStatus.user_id == user_id,
                ),
            )
            .values(count=MessageReadStatus.count + 1)
        )
        await self.session.execute(stmt)
        await self.session.commit()


async def update_mark_read_message(
    session: AsyncSession,
    task_id: int,
    user_id: int,
) -> None:
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
