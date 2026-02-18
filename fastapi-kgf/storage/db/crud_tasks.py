from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from core.models import Task
from core.types.tasks import TaskStatus


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
    # Сначала получаем объект
    result = await get_task_by_title(session=session, title=title)

    if result:
        await session.delete(result)  # ORM-удаление
        await session.commit()


async def update_status_task(session: AsyncSession, title: str, status: str):
    stmt = update(Task).where(Task.title == title).values(status=status)
    await session.execute(stmt)
    await session.commit()
