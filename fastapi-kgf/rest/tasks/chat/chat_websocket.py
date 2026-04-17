import json
from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.models import db_helper
from dependencies.message import get_message_service
from dependencies.providers import get_user_service
from services.messages.connection_service import connectionmanager
from services.messages.message_service import MessageManager
from services.users.service import UserService

router = APIRouter()


@router.websocket("/ws/task/{task_id}/{user_id}", name="chat:task")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    user_id: int,
    message_service: Annotated[MessageManager, Depends(get_message_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> None:
    await connectionmanager.connect(websocket, task_id, user_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_date = json.loads(data)

            user = await user_service.get_user_by_id(
                int(message_date["author"]),
            )

            file_folder = await message_service.add_message_in_db(message_date)

            if user:
                user_name = await user.awaitable_attrs.name
                user_surname = await user.awaitable_attrs.surname

                # Формируем нужные строки
                full_name = f"{user_name} {user_surname}".strip()
                initials = f"{user_name[0]}{user_surname[0]}".upper()
            else:
                full_name = "No Name"
                initials = "NN"

            # Обновляем данные для рассылки
            message_date.update(
                initials=initials,
                author=full_name,
            )

            if file_folder:
                message_date["file"].pop("content")
                message_date.update(
                    file={
                        "name": message_date["file"]["name"],
                        "folder_path": file_folder,
                    },
                )

            # Рассылаем всем в этой задаче (включая отправителя)
            await connectionmanager.broadcast(
                json.dumps(message_date),
                task_id,
                session,
            )

    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket, task_id, user_id)
