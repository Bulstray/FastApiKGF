from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        # Словарь для соединений по комнатам (task_id)
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: int) -> None:
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = []
        self.active_connections[task_id].append(websocket)

    def disconnect(self, websocket: WebSocket, task_id: int) -> None:
        if task_id in self.active_connections:
            self.active_connections[task_id].remove(websocket)
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]

    async def broadcast(self, message: str, task_id: int) -> None:
        """Отправить сообщение всем в задаче"""
        if task_id in self.active_connections:
            for connection in self.active_connections[task_id]:
                await connection.send_text(message)


connectionmanager = ConnectionManager()
