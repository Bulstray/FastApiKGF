from typing import Annotated, cast

from fastapi import Depends, UploadFile
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from dependencies.projects import get_project_service
from dependencies.providers import get_tasks_service
from services.projects.service import ProjectService
from services.task import TasksFilesService

from fastapi import APIRouter

router = APIRouter()


@router.post("/{project_id}", name="tasks:post")
async def create_task(
    request: Request,
    project_id: int,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> RedirectResponse:

    project = await project_service.get_by_id(project_id)
    if project is None:
        return RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    async with request.form() as form:
        content = await cast(UploadFile, form.get("rar_file")).read()

        await service.create_task(
            form=form,
            content=content,
        )

    return RedirectResponse(
        url=f"/projects/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
