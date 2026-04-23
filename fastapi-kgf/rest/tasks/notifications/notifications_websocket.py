from fastapi import APIRouter, WebSocketException, WebSocket, WebSocketDisconnect

from services.notification.connection_manager import manager

router = APIRouter()


@router.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(
    websocket: WebSocket,
    user_id: int,
) -> None:
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()

    except (WebSocketDisconnect, WebSocketException):
        manager.disconnect(user_id=user_id)
