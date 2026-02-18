from typing import List, Dict
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
import json

from sqlalchemy.ext.asyncio import AsyncSession

from storage.db import crud_message

from core.models import ChatsMessage, db_helper
from typing import Annotated

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        # Словарь для соединений по комнатам (task_id)
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: int):
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = []
        self.active_connections[task_id].append(websocket)
        print(f"Клиент подключился к задаче {task_id}")

    def disconnect(self, websocket: WebSocket, task_id: int):
        if task_id in self.active_connections:
            self.active_connections[task_id].remove(websocket)
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]
        print(f"Клиент отключился от задачи {task_id}")

    async def broadcast(self, message: str, task_id: int):
        """Отправить сообщение всем в задаче"""
        if task_id in self.active_connections:
            for connection in self.active_connections[task_id]:
                try:
                    await connection.send_text(message)
                except:
                    pass


connectionmanager = ConnectionManager()


@router.websocket("/ws/task/{task_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    await connectionmanager.connect(websocket, task_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_date = json.loads(data)

            message_in = ChatsMessage(
                task_id=task_id,
                author=message_date["author"],
                time=message_date["time"],
                text=message_date["text"],
                initials="".join([elem[0] for elem in message_date["author"].split()]),
            )

            await crud_message.create_chats_message(session, message_in)

            # Рассылаем всем в этой задаче (включая отправителя)
            await connectionmanager.broadcast(data, task_id)

    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket, task_id)
