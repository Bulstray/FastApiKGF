from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from core.models import Task


async def get_all_tasks(session: AsyncSession):
    stmt = select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_task_by_title(session: AsyncSession, title: str):
    stmt = select(Task).where(Task.title == title)
    result = await session.scalars(stmt)
    return result.first()


async def create_file_in_db(
    session: AsyncSession,
    task: Task,
) -> Task:
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_tasks_in_db(session: AsyncSession, title):
    stmt = delete(Task).where(Task.title == title)
    await session.execute(stmt)
    await session.commit()
