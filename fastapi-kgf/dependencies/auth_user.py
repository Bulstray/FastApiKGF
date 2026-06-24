from typing import Annotated

import bcrypt
from fastapi import Depends, Request

from core.schemas import UserLogin
from services.auth.session_manager import create_session
from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserServiceFactory

from storage.db.crud_user import get_user_by_email


async def validate_basic_auth_user(
    request: Request,
    session: AsyncSession,
) -> str | None:
    async with request.form() as form_data:
        user = UserLogin.model_validate(form_data)

    is_user = await get_user_by_email(
        session,
        user.email.lower(),
    )

    if is_user and bcrypt.checkpw(
        password=user.password.encode("utf-8"),
        hashed_password=is_user.hashed_password.encode("utf-8"),
    ):

        return await create_session(is_user)

    return None
