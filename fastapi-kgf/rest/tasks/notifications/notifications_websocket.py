from fastapi import (
    APIRouter,
    WebSocketException,
    WebSocket,
    WebSocketDisconnect,
)

from managers.notification_manager import notification_manager

router = APIRouter()


@router.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(
    websocket: WebSocket,
    user_id: int,
) -> None:
    await notification_manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()

    except (WebSocketDisconnect, WebSocketException):
        notification_manager.disconnect(user_id=user_id)
