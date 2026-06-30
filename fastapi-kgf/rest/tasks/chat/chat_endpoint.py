from typing import Annotated

from aiopath import AsyncPath
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from dependencies import TaskMessageFactory
from storage.db import crud_message
from utils import get_file_size

from core.schemas.messages import MessageRead
from core.models import Message

router = APIRouter()


@router.get(
    "/chat/{task_id}",
    name="message:task",
    response_model=list[MessageRead],
)
async def get_messages_by_id(
    task_id: int,
    message_service: Annotated[
        TaskMessageFactory,
        Depends(TaskMessageFactory),
    ],
) -> list[Message]:

    return await message_service.get_messages_for_task(
        task_id,
    )


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
