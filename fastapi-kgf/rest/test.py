import json
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from dependencies.message import get_message_service
from services.messages.connection_service import connectionmanager
from services.messages.message_service import MessageManager

router = APIRouter()


@router.websocket("/ws/task/{task_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    message_service: Annotated[MessageManager, Depends(get_message_service)],
):
    await connectionmanager.connect(websocket, task_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_date = json.loads(data)

            await message_service.add_message_in_db(
                message_data=message_date,
                task_id=task_id,
            )

            # Рассылаем всем в этой задаче (включая отправителя)
            await connectionmanager.broadcast(data, task_id)

    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket, task_id)
