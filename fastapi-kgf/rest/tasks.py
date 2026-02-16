from fastapi import APIRouter, Request, Depends, Form, UploadFile, status
from fastapi.responses import RedirectResponse, FileResponse

from templating.jinja_template import templates
from dependencies.session_auth import require_auth

from typing import Annotated
from core.schemas.user import UserRead
from dependencies.providers import get_tasks_service, get_user_service
from services.files.tasks_files.service import TasksFilesService

from core.schemas.tasks import TaskCreate
from core.models import Task

from core.config import settings

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.users.service import UserService
    from services.files.tasks_files.service import TasksFilesService


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
    title: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    deadline: Annotated[str, Form(...)],
    executor: Annotated[str, Form(...)],
    customer: Annotated[str, Form(...)],
    rar_file: UploadFile | None = None,
):

    task = TaskCreate(
        title=title,
        description=description,
        executor=executor,
        customer=customer,
        deadline=deadline,
        file=rar_file.filename,
    )

    await service.create_task(
        task=task,
        file=rar_file,
    )

    return RedirectResponse(
        url="/tasks",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("delete/{title}/", name="task:delete")
async def delete_task(
    title: str,
    service: Annotated[TasksFilesService, Depends(get_tasks_service)],
):
    await service.delete_task(title)

    return RedirectResponse(
        url="/tasks",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("download/{name}/", name="task:download")
async def download_file(
    name: str,
    request: Request,
):
    return FileResponse(
        rf"{settings.uploads_file_task_dir}/{name}",
        filename=name,
    )
