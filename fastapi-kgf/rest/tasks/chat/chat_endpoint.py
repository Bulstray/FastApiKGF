import json
from typing import Annotated

from aiopath import AsyncPath
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from core.models import db_helper
from dependencies.message import get_message_service
from dependencies.providers import get_user_service

from services.messages.connection_service import connectionmanager
from services.messages.message_service import MessageManager
from services.users.service import UserService
from storage.db import crud_message
from utils import get_file_size

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

            message_date.update(
                initials=user.initials,
                author=user.full_name,
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


@router.get("/chat/{task_id}", name="message:task")
async def get_messages_by_id(
    task_id: int,
    message_service: Annotated[MessageManager, Depends(get_message_service)],
):

    messages = await message_service.get_messages_by_id(
        task_id,
    )

    messages_dict = []

    for message in messages:
        msg = {
            "id": message.id,
            "text": message.text,
            "author": message.user_message.full_name,
            "created_at": message.created_at,
            "initials": message.user_message.initials,
        }

        if message.file:

            size = await get_file_size(AsyncPath(message.file.folder_path))
            msg.update(
                file={
                    "name": message.file.name,
                    "folder_path": message.file.folder_path,
                    "size": size,
                },
            )

        messages_dict.append(msg)

    return messages_dict


@router.post("/mark_read/{task_id}/{user_id}", name="message:mark_read")
async def mark_read(
    task_id: int,
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> None:
    await crud_message.update_mark_read_message(
        session=session,
        task_id=task_id,
        user_id=user_id,
    )
