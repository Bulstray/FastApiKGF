from typing import Annotated

from aiopath import AsyncPath
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from dependencies.message import get_message_service

from services.messages.message_service import MessageManager
from storage.db import crud_message
from utils import get_file_size

router = APIRouter()


@router.get("/chat/{task_id}", name="message:task")
async def get_messages_by_id(
    task_id: int,
    message_service: Annotated[MessageManager, Depends(get_message_service)],
):

    messages = await message_service.get_messages_by_id(
        task_id,
    )

    messages_list = []

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

        messages_list.append(msg)

    return messages_list


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
