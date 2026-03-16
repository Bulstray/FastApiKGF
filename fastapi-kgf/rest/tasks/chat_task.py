import json
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from dependencies.message import get_message_service
from services.messages.connection_service import connectionmanager
from services.messages.message_service import MessageManager

from storage.db import crud_message
from core.models import db_helper

router = APIRouter()


@router.websocket("/ws/task/{task_id}", name="chat:task")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    message_service: Annotated[MessageManager, Depends(get_message_service)],
) -> None:
    await connectionmanager.connect(websocket, task_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_date = json.loads(data)

            await message_service.add_message_in_db(
                message_data=message_date,
            )

            # Рассылаем всем в этой задаче (включая отправителя)
            await connectionmanager.broadcast(data, task_id)

    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket, task_id)


@router.get("/chat/{task_id}", name="message:task")
async def get_message_by_id(
    task_id: int,
    message_service: Annotated[MessageManager, Depends(get_message_service)],
):

    messages = await message_service.get_messages_by_id(
        task_id,
    )

    return messages


@router.post("/mark_read/{task_id}", name="message:mark_read")
async def mark_read(
    task_id: int, session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    await crud_message.update_mark_read_message(session, task_id)


@router.get("/unread", name="message:unread")
async def get_unread(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    res = await crud_message.count_unread_messages(session)
    return res


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Отправить всем подключенным клиентам"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()

#
# @router.websocket("/ws/notifications")
# async def websocket_notifications(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             # Ждем сообщения от клиента (если нужно)
#             await websocket.receive_text()
#
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
