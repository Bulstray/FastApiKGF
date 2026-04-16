from starlette.websockets import WebSocket, WebSocketDisconnect

from fastapi import APIRouter
from services.notification.connection_manager import manager

router = APIRouter()


@router.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(websocket: WebSocket, user_id: int) -> None:
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(user_id=user_id)
