from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from storage.db import crud_message

from core.schemas.messages import MessageRead
from core.models import Message, db_helper

router = APIRouter()


@router.get(
    "/chat/{task_id}",
    name="message:task",
    response_model=list[MessageRead],
)
async def get_messages_by_id(
    task_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> list[Message]:

    return await crud_message.get_messages_for_task(
        session,
        task_id,
    )


@router.post(
    "/mark_read/{task_id}/{user_id}",
    name="message:mark_read",
)
async def mark_read(
    task_id: int,
    user_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:
    await crud_message.update_mark_read_message(
        session=session,
        task_id=task_id,
        user_id=user_id,
    )
