from fastapi import APIRouter, Depends, status

from typing import Annotated, TYPE_CHECKING

from starlette.responses import RedirectResponse

from dependencies.projects import get_project_service

if TYPE_CHECKING:
    from services.projects.service import ProjectService


router = APIRouter()


@router.post("/{project_id}/delete")
async def delete_project(
    project_id: int,
    service: Annotated["ProjectService", Depends(get_project_service)],
):
    await service.delete_project(project_id)

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
