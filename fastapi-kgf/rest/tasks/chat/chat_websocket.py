import json
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.models import db_helper
from core.schemas import UserRead
from dependencies import TaskMessageFactory
from managers.message_manager import message_manager
from storage.db import crud_user

router = APIRouter()


@router.websocket("/ws/task/{task_id}/{user_id}", name="chat:task")
async def websocket_endpoint(
    websocket: WebSocket,
    task_id: int,
    user_id: int,
    message_service: Annotated[
        TaskMessageFactory,
        Depends(TaskMessageFactory),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:

    await message_manager.connect(websocket, task_id, user_id)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()

            message_data = await message_service.process_message(data)

            user = UserRead.model_validate(
                await crud_user.get_user_by_id(
                    session,
                    int(message_data["author"]),
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
