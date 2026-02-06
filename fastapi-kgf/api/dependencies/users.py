from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User


async def get_user_db(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    yield User.get_db(session=session)
