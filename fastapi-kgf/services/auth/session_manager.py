import uuid
from typing import Annotated

from fastapi import Depends

from core.models import User
from core.schemas import UserRead
from dependencies.session_auth import cookie_scheme
from storage.redis import session


async def create_session(user: User) -> str:
    return await session.save_session(
        session_id=f"{uuid.uuid4().hex}",
        user=UserRead.model_validate(user),
    )


async def delete_session(
    session_id: Annotated[
        str | None,
        Depends(cookie_scheme),
    ],
) -> None:

    if session_id:
        await session.delete_by_session_id(
            session_id=session_id,
        )
