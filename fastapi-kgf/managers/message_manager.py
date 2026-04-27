from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket

from storage.db.crud_message import update_mark_read_message
from storage.db.crud_task_users import get_task_users

from .notification_manager import notification_manager


class ConnectionManager:
    def __init__(self) -> None:
        # Словарь для соединений по комнатам (task_id)
        self.active_connections: dict[int, tuple[int, WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        task_id: int,
        user_id: int,
    ) -> None:
        await websocket.accept()

        self.active_connections[task_id] = self.active_connections.get(task_id, []) + [
            (user_id, websocket),
        ]

    async def disconnect(
        self,
        websocket: WebSocket,
        task_id: int,
        user_id: int,
    ) -> None:
        try:
            self.active_connections[task_id].remove((user_id, websocket))
        except (ValueError, KeyError):
            return
        else:
            if not self.active_connections[task_id]:
                self.active_connections.pop(task_id)

    async def broadcast(
        self,
        message: str,
        task_id: int,
        session: AsyncSession,
    ) -> None:
        users_task = await get_task_users(session, task_id)

        if task_id in self.active_connections:
            for user_id, connection in self.active_connections[task_id]:

                await connection.send_text(message)

                await update_mark_read_message(
                    session=session,
                    task_id=task_id,
                    user_id=user_id,
                )

                users_task.remove(user_id)

            await notification_manager.broadcast(users_task, task_id)


message_manager = ConnectionManager()
