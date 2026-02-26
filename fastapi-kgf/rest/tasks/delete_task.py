from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from core.schemas.user import UserRead
from dependencies.providers import get_tasks_service
from dependencies.session_auth import require_auth
from services.task import TasksFilesService

router = APIRouter(prefix="/delete_task")


@router.get("/{task_id}", name="tasks:delete")
async def delete_task(
    task_id: int,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
):
    await service.delete_task(
        id_task=task_id,
    )

    return RedirectResponse(
        url="/tasks",
        status_code=status.HTTP_303_SEE_OTHER,
    )
