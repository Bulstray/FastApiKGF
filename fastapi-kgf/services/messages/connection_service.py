from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from services.notification.connection_manager import manager
from storage.db.crud_message import update_mark_read_message
from storage.db.crud_task_users import get_task_users


class ConnectionManager:
    def __init__(self) -> None:
        # Словарь для соединений по комнатам (task_id)
        self.active_connections: dict[int, list[int, WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        task_id: int,
        user_id: int,
    ) -> None:
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = []
        self.active_connections[task_id].append([user_id, websocket])

    def disconnect(
        self,
        websocket: WebSocket,
        task_id: int,
        user_id: int,
    ) -> None:
        if task_id in self.active_connections:
            self.active_connections[task_id].remove([user_id, websocket])
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]

    async def broadcast(
        self,
        message: str,
        task_id: int,
        session: AsyncSession,
    ) -> None:
        """Отправить сообщение всем в задаче"""

        users_task = await get_task_users(session, task_id)

        if task_id in self.active_connections:
            for user_id, connection in self.active_connections[task_id]:

                await connection.send_text(message)

                await update_mark_read_message(
                    session=session,
                    task_id=task_id,
                    user_id=user_id,
                )

                if user_id in users_task:
                    users_task.remove(user_id)

            await manager.broadcast(users_task, task_id)


connectionmanager = ConnectionManager()
