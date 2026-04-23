import json

from fastapi import (
    APIRouter,
    WebSocketException,
    WebSocket,
    WebSocketDisconnect,
)
from services.tasks_page.connection_manager import manager

router = APIRouter()


@router.websocket("/ws/action/{project_id}")
async def action_tasks(websocket: WebSocket, project_id: int) -> None:
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

    except (WebSocketDisconnect, WebSocketException):
        await manager.disconnect(project_id, websocket)
