from typing import Annotated, cast

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import RedirectResponse

from dependencies import ProjectFactory
from dependencies import TaskFactory
from services import ProjectService

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
    service: Annotated[TaskFactory, Depends(TaskFactory)],
    project_service: Annotated[ProjectService, Depends(ProjectFactory)],
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
