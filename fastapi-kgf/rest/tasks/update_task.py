from typing import Annotated

from fastapi import APIRouter, Depends

from core.schemas.user import UserRead
from dependencies.providers import get_tasks_service
from dependencies.session_auth import require_auth
from services.task import TasksFilesService

router = APIRouter(prefix="/update_task")


@router.post("/{title}/{status_task}", name="tasks:update:status")
async def update_status_task(
    title: str,
    status_task: str,
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
) -> None:
    await service.update_status_in_db(
        title=title,
        status=status_task,
    )
