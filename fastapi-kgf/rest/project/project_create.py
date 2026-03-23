from fastapi import APIRouter, Depends, Request, status
from starlette.responses import RedirectResponse

from dependencies.projects import get_project_service
from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from services.projects.service import ProjectService


router = APIRouter()


@router.post("/", name="project:create")
async def create_project(
    request: Request,
    service: Annotated["ProjectService", Depends(get_project_service)],
):
    async with request.form() as form:
        project = await service.create_project(form)

    return RedirectResponse(
        url=f"/tasks/{project.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
