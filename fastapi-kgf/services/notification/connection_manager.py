from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.update({user_id: websocket})

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id)

    async def broadcast(self, users_id: list[int], task_id: int):
        """Отправить всем подключенным клиентам"""
        for user_id in users_id:
            if user_id in self.active_connections:
                await self.active_connections[user_id].send_json({"task_id": task_id})


manager = ConnectionManager()
