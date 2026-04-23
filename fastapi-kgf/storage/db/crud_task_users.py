from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.taks_users import TaskUsers


async def get_task_users(session: AsyncSession, task_id: int) -> list[int]:
    """Получить всех исполнителей задачи"""
    stmt = select(TaskUsers.user_id).where(TaskUsers.task_id == task_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())
