from sqlalchemy.ext.asyncio import AsyncSession

from core.models.taks_users import TaskUsers
from core.schemas.tasks_users import TaskUsersCreate


async def create_task_users(
    session: AsyncSession,
    task_users: TaskUsersCreate,
) -> None:
    for executor_id in task_users.executor_ids:
        session.add(
            TaskUsers(
                task_id=task_users.task_id,
                user_id=executor_id,
            )
        )

    await session.commit()
