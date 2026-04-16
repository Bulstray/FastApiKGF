from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from dependencies.projects import get_project_service
from services.projects.service import ProjectService
from services.tasks_page.connection_manager import manager


router = APIRouter()


@router.post("/{project_id}/delete")
async def delete_project(
    project_id: int,
    service: Annotated[
        "ProjectService",
        Depends(get_project_service),
    ],
):
    await service.delete_project(project_id)
    await manager.delete_project_id(project_id)

    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
