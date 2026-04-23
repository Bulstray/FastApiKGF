from sqlalchemy import select, update, case, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, TaskUsers, MessageReadStatus
from core.schemas import TaskRead

from core.types.tasks import TaskStatus


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


async def add_task(
    session: AsyncSession,
    task_in: TaskRead,
    user_ids: list[int],
) -> None:
    task_model = Task(**task_in.model_dump())
    session.add(task_model)

    await session.flush()

    task_users = [
        TaskUsers(task_id=task_model.id, user_id=user_id) for user_id in user_ids
    ]

    session.add_all(task_users)

    unread_statuses = [
        MessageReadStatus(task_id=task_model.id, user_id=user_id)
        for user_id in user_ids
    ]

    session.add_all(unread_statuses)

    await session.commit()


async def delete_tasks_in_db(
    session: AsyncSession,
    task: Task,
) -> None:
    # Сначала получаем объект
    await session.delete(task)  # ORM-удаление
    await session.commit()


async def delete_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> None:
    task = await session.get(Task, task_id)
    if task:
        await delete_tasks_in_db(session, task)


async def update_status_task(
    session: AsyncSession,
    id_task: int,
) -> None:
    stmt = (
        update(Task)
        .where(Task.id == id_task)
        .values(
            status=case(
                (Task.status == TaskStatus.NOT_STARTED, TaskStatus.STARTED),
                (Task.status == TaskStatus.STARTED, TaskStatus.COMPLETED),
                (Task.status == TaskStatus.COMPLETED, TaskStatus.NOT_STARTED),
            )
        )
    )
    await session.execute(stmt)
    await session.commit()


async def get_tasks_by_project_id(
    session: AsyncSession,
    project_id: int,
    user_id: int,
):
    stmt = (
        select(Task)
        .join(TaskUsers, Task.id == TaskUsers.task_id)
        .where(
            and_(
                Task.project_id == project_id,
                TaskUsers.user_id == user_id,
            )
        )
    )
    result = await session.scalars(stmt)
    return list(result.all())
