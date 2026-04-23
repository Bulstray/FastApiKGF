from starlette.websockets import WebSocket
from storage.db.crud_tasks import update_status_task, delete_task_by_id


from core.models import db_helper


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: int) -> None:
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

    async def disconnect(self, project_id: int, websocket: WebSocket) -> None:
        try:
            self.active_connections[project_id].remove(websocket)
        except KeyError:
            pass

    async def delete_project_id(self, project_id: int) -> None:
        try:
            self.active_connections.pop(project_id)
        except KeyError:
            pass

    async def broadcast(
        self,
        project_id: int,
        task_id: int,
        method: str,
    ) -> None:

        async with db_helper.session_factory() as session:

            if method == "update":
                await update_status_task(session, task_id)
            elif method == "delete":
                await delete_task_by_id(session, task_id)

        """Отправить всем подключенным клиентам"""
        for connection in self.active_connections[project_id]:
            await connection.send_json(
                {
                    "action": method,
                    "task_id": task_id,
                }
            )


manager = ConnectionManager()
