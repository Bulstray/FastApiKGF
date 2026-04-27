from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.users.service import UserService


async def get_user_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return UserService(session)
