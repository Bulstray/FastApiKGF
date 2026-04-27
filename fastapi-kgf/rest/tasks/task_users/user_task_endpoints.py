from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from storage.db import crud_task_users

router = APIRouter()


@router.get("/user_tasks/{task_id}")
async def get_users_for_task(
    task_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud_task_users.get_task_users(session, task_id)
