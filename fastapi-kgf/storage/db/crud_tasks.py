from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.tasks import Task as TaskSchema


async def get_all_tasks(
    session: AsyncSession,
) -> list[Task]:
    stmt = select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    return await session.get(Task, task_id)


async def create_file_in_db(
    session: AsyncSession,
    task_in: TaskSchema,
) -> int:
    task = Task(**task_in.model_dump())

    session.add(task)
    await session.commit()
    await session.refresh(task)
    task_id = task.id
    return task_id


async def delete_tasks_in_db(
    session: AsyncSession,
    task: Task,
) -> None:
    # Сначала получаем объект
    await session.delete(task)  # ORM-удаление
    await session.commit()


async def update_status_task(
    session: AsyncSession,
    id_task: str,
    status: str,
) -> None:
    stmt = update(Task).where(Task.id == id_task).values(status=status)
    await session.execute(stmt)
    await session.commit()


async def get_tasks_by_project_id(
    session: AsyncSession,
    project_id: int,
):
    stmt = select(Task).where(Task.project_id == project_id)
    result = await session.scalars(stmt)
    return list(result.all())
