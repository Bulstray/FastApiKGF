from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.schemas.tasks import TaskCreate
from dependencies.providers import get_tasks_service
from services.task import TasksFilesService


router = APIRouter()


@router.post("/", name="tasks:post")
async def create_task(
    request: Request,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
):

    async with request.form() as form:
        task = TaskCreate.model_validate(form)
        content = await form.get("rar_file").read()

    await service.create_task(
        task_in=task,
        content=content,
    )

    return RedirectResponse(
        url="/tasks",
        status_code=status.HTTP_303_SEE_OTHER,
    )
