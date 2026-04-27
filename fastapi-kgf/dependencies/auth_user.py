from typing import Annotated

import bcrypt
from fastapi import Depends, Request

from core.models import User
from core.schemas import UserLogin
from services.auth.session_manager import create_session
from services.users.service import UserService

from .user import get_user_service


async def validate_basic_auth_user(
    request: Request,
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> str | None:
    async with request.form() as form_data:
        user = UserLogin.model_validate(form_data)

    is_user: None | User = await user_service.get_user_by_username(
        username=user.username,
    )

    if is_user and bcrypt.checkpw(
        password=user.password.encode("utf-8"),
        hashed_password=is_user.hashed_password.encode("utf-8"),
    ):

        return await create_session(is_user)

    return None
