from typing import Annotated, cast, TYPE_CHECKING

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from dependencies import ProjectFactory, TaskFactory
from services import ProjectService

if TYPE_CHECKING:
    from fastapi import UploadFile

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
        file = cast("UploadFile", form.get("rar_file"))
        content = await file.read()

        await service.create_task(
            form=form,
            content=content,
        )

    return f"/projects/{project_id}"
