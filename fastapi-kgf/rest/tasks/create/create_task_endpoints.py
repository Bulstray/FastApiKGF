from typing import Annotated, cast

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse

from dependencies.projects import get_project_service
from dependencies.providers import get_tasks_service
from services import ProjectService, TasksFilesService

router = APIRouter()


@router.post(
    "/{project_id}",
    name="tasks:post",
    response_class=RedirectResponse,
    status_code=status.HTTP_303_SEE_OTHER,
)
async def create_task(
    request: Request,
    project_id: int,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> str:

    project = await project_service.get_by_id(project_id)
    if project is None:
        return "/"

    async with request.form() as form:
        content = await cast("UploadFile", form.get("rar_file")).read()

        await service.create_task(
            form=form,
            content=content,
        )

    return f"/projects/{project_id}"
