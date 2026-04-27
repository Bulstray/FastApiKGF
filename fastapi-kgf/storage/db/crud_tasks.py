from sqlalchemy import and_, case, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, TaskUsers
from core.types.tasks import TaskStatus

from .base_crud import BaseCRUD


class TaskStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Task)

    async def get_user_tasks_by_project_id(
        self,
        project_id: int,
        user_id: int,
    ) -> list[Task]:
        stmt = (
            select(Task)
            .join(TaskUsers, Task.id == TaskUsers.task_id)
            .where(
                and_(
                    Task.project_id == project_id,
                    TaskUsers.user_id == user_id,
                ),
            )
        )
        result = await self.session.scalars(stmt)
        return list(result.all())


async def delete_task_by_id(
    session: AsyncSession,
    task_id: int,
) -> None:
    task = await session.get(Task, task_id)
    if task:
        await session.delete(task)  # ORM-удаление
        await session.commit()


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
            ),
        )
    )
    await session.execute(stmt)
    await session.commit()


async def get_tasks_by_project_id(
    session: AsyncSession,
    project_id: int,
    user_id: int,
) -> list[Task]:
    stmt = (
        select(Task)
        .join(TaskUsers, Task.id == TaskUsers.task_id)
        .where(
            and_(
                Task.project_id == project_id,
                TaskUsers.user_id == user_id,
            ),
        )
    )
    result = await session.scalars(stmt)
    return list(result.all())
