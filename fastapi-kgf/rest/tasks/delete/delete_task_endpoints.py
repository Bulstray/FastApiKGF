from typing import Annotated

from fastapi import Depends, Query, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from core.schemas.user import UserRead
from dependencies.providers import get_tasks_service
from dependencies.session_auth import require_auth
from services.task import TasksFilesService

router = APIRouter()


@router.get("/{task_id}", name="tasks:delete")
async def delete_task(
    task_id: int,
    service: Annotated["TasksFilesService", Depends(get_tasks_service)],
    is_auth_user: Annotated["UserRead", Depends(require_auth)],
    return_url: str = Query(None),
) -> RedirectResponse:
    await service.delete_task(
        id_task=task_id,
    )

    return RedirectResponse(
        url=return_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )
