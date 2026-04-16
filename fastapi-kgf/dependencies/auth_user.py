import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated
from fastapi import Depends, Request

from core.models import db_helper

from core.models import User
from storage.db import crud_user

from services.auth.session_manager import create_session


async def validate_basic_auth_user(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> str | None:
    async with request.form() as form_data:
        is_user: None | User = await crud_user.get_user_by_username(
            session=session,
            username=form_data["username"],
        )

        if is_user and bcrypt.checkpw(
            password=form_data["password"].encode("utf-8"),
            hashed_password=is_user.hashed_password.encode("utf-8"),
        ):

            return await create_session(is_user)

        return None
