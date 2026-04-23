import json
from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.models import db_helper
from core.schemas import Message, UserRead
from dependencies.message import get_message_service
from dependencies.providers import get_user_service
from managers.message_manager import message_manager
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
    await message_manager.connect(websocket, task_id, user_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message_schema = Message.model_validate(
                json.loads(data),
            )

            user = UserRead.model_validate(
                await user_service.get_by_id(
                    message_schema.author,
                )
            )

            file_folder = await message_service.process_message(message_schema)

            # Обновляем данные для рассылки
            message_data = message_schema.model_dump(exclude={"file"})
            message_data.update(
                {
                    "author": user.full_name,
                    "initials": user.initials,
                }
            )

            if message_schema.file:
                message_data.update(
                    file={
                        "name": message_schema.file.name,
                        "folder_path": file_folder,
                    },
                )

            # Рассылаем всем в этой задаче (включая отправителя)
            await message_manager.broadcast(
                json.dumps(message_data),
                task_id,
                session,
            )

    except WebSocketDisconnect:
        await message_manager.disconnect(websocket, task_id, user_id)
