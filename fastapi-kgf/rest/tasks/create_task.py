from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from dependencies.providers import get_tasks_service
from services.task import TasksFilesService
from typing import cast

router = APIRouter()


@router.post("/{project_id}", name="tasks:post")
async def create_task(
    request: Request,
    project_id: int,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
) -> RedirectResponse:

    async with request.form() as form:
        content = cast(UploadFile, form.get("rar_file")).read()

        await service.create_task(
            form=form,
            content=content,
        )

    return RedirectResponse(
        url=f"/tasks/{project_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
