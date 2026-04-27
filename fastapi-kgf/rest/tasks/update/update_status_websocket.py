import json

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)

from managers.task_event_manager import task_event_manager

router = APIRouter()


@router.websocket("/ws/action/{project_id}")
async def action_tasks(websocket: WebSocket, project_id: int) -> None:
    await task_event_manager.connect(websocket, project_id)
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            await task_event_manager.broadcast(
                project_id,
                task_id=json_data["task_id"],
                method=json_data["action"],
            )

    except (WebSocketDisconnect, WebSocketException):
        await task_event_manager.disconnect(project_id, websocket)
