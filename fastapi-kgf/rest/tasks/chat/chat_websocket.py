import json
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.models import db_helper
from core.schemas import UserRead
from dependencies import TaskMessageFactory, UserServiceFactory
from managers.message_manager import message_manager
from services import MessageManager, UserService

router = APIRouter()


async def _build_services(
    message_service: Annotated[
        TaskMessageFactory,
        Depends(TaskMessageFactory),
    ],
    user_service: Annotated[
        UserServiceFactory,
        Depends(UserServiceFactory),
    ],
) -> tuple[MessageManager, UserService]:
    return message_service, user_service


@router.websocket("/ws/task/{task_id}/{user_id}", name="chat:task")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    user_id: int,
    services: Annotated[
        tuple[MessageManager, UserService],
        Depends(_build_services),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:
    message_service, user_service = services

    await message_manager.connect(websocket, task_id, user_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()

            message_data = await message_service.process_message(data)

            user = UserRead.model_validate(
                await user_service.get_by_id(
                    message_data["author"],
                ),
            )

            message_data.update(
                author=user.full_name,
                initials=user.initials,
            )

            # Рассылаем всем в этой задаче (включая отправителя)
            await message_manager.broadcast(
                json.dumps(message_data),
                task_id,
                session,
            )

    except WebSocketDisconnect:
        await message_manager.disconnect(websocket, task_id, user_id)
