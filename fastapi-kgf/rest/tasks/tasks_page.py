import datetime
import json
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from dependencies.message import get_message_service
from dependencies.providers import get_tasks_service, get_user_service
from dependencies.session_auth import require_auth
from dependencies.projects import get_project_service
from templating.jinja_template import templates
from services.tasks_page.connection_manager import manager

if TYPE_CHECKING:
    from core.schemas.user import UserRead
    from services.messages.message_service import MessageManager
    from services.task import TasksFilesService
    from services.users.service import UserService
    from services.projects.service import ProjectService

router = APIRouter()


@router.get("/{project_id}", name="tasks:page")
async def tasks_page(
    request: Request,
    project_id: int,
    is_auth_user: Annotated["UserRead", Depends(require_auth)],
    user_service: Annotated["UserService", Depends(get_user_service)],
    tasks_service: Annotated["TasksFilesService", Depends(get_tasks_service)],
    message_service: Annotated["MessageManager", Depends(get_message_service)],
    project_service: Annotated["ProjectService", Depends(get_project_service)],
) -> HTMLResponse:
    unread_messages = await message_service.get_unread_message(is_auth_user.id)
    workers = await user_service.get_all_users()
    tasks = await tasks_service.get_tasks_by_project_id(project_id)
    projects = await project_service.get_all_projects()
    project = await project_service.get_project_by_id(project_id)

    context = {
        "workers": workers,
        "user": is_auth_user,
        "tasks": tasks,
        "unread_messages": unread_messages,
        "projects": projects,
        "project_id": project_id,
        "project": project,
        "today": datetime.date.today(),
    }

    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
        context=context,
    )


@router.websocket("/ws/action/{project_id}")
async def action_tasks(websocket: WebSocket, project_id: int):
    await manager.connect(websocket, project_id)
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            await manager.broadcast(
                project_id,
                task_id=json_data["task_id"],
                method=json_data["action"],
            )

    except Exception:
        manager.disconnect(project_id, websocket)
