from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Form, Request, UploadFile, status
from fastapi.responses import FileResponse, RedirectResponse

from core.config import settings
from core.schemas.tasks import TaskCreate
from core.schemas.user import UserRead
from dependencies.providers import get_tasks_service, get_user_service
from dependencies.session_auth import require_auth
from services.files.tasks_files.service import TasksFilesService
from templating.jinja_template import templates

if TYPE_CHECKING:
    from services.files.tasks_files.service import TasksFilesService
    from services.users.service import UserService


router = APIRouter(prefix="/tasks")


@router.get("/", name="tasks:page")
async def tasks_page(
    request: Request,
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
    user_service: Annotated["UserService", Depends(get_user_service)],
    tasks_service: Annotated["TasksFilesService", Depends(get_tasks_service)],
):
    workers = await user_service.get_all_users()
    tasks = await tasks_service.get_tasks()
    context = {
        "workers": workers,
        "user": is_auth_user,
        "tasks": tasks,
    }

    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
        context=context,
    )


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


@router.get("delete/{task_id}/", name="task:delete")
async def delete_task(
    task_id: int,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
):
    await service.delete_task(
        id_task=task_id,
    )

    return RedirectResponse(
        url="/tasks",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("download/{name}/{file_path:path}", name="task:download")
async def download_file(
    name: str,
    file_path: str,
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
):
    return FileResponse(
        file_path,
        filename=name,
    )


@router.post("/update/{title}/{status_task}", name="task:update:status")
async def update_status_task(
    title: str,
    status_task: str,
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
):
    await service.update_status_in_db(
        title=title,
        status=status_task,
    )


@router.get("download_chat/{file_path:path}", name="task:download:chat")
async def download_chat_file_by_id(file_path: str):
    file_name = file_path.split("/")[-1]
    return FileResponse(
        str(file_path),
        filename=file_name,
    )
