from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task


async def get_all_tasks(session: AsyncSession):
    stmt = select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_task_by_id(session: AsyncSession, task_id: int):
    result = await session.get(Task, task_id)
    return result


async def create_file_in_db(
    session: AsyncSession,
    task: Task,
) -> Task:
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_tasks_in_db(session: AsyncSession, task: Task):
    # Сначала получаем объект
    await session.delete(task)  # ORM-удаление
    await session.commit()


async def update_status_task(session: AsyncSession, title: str, status: str):
    stmt = update(Task).where(Task.title == title).values(status=status)
    await session.execute(stmt)
    await session.commit()
