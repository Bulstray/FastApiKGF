from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import RedirectResponse

from dependencies.projects import get_project_service
from managers.task_event_manager import task_event_manager
from services.projects.service import ProjectService

router = APIRouter()


@router.post("/{project_id}/delete")
async def delete_project(
    project_id: int,
    project_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
) -> RedirectResponse:
    await project_service.delete_by_id(project_id)
    await task_event_manager.delete_project_id(project_id)

    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
