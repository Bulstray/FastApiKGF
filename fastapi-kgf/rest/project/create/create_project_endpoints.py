from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from dependencies.projects import get_project_service
from services.projects.service import ProjectService

router = APIRouter()


@router.post("/", name="project:create")
async def create_project(
    request: Request,
    service: Annotated["ProjectService", Depends(get_project_service)],
) -> RedirectResponse:
    async with request.form() as form:
        project = await service.create_project(form)

    return RedirectResponse(
        url=f"/projects/{project.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
