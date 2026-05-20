from typing import Annotated

import bcrypt
from fastapi import Depends, Request

from core.schemas import UserLogin
from services.auth.session_manager import create_session

from .user import UserServiceFactory


async def validate_basic_auth_user(
    request: Request,
    user_service: Annotated[
        UserServiceFactory,
        Depends(UserServiceFactory.init_user_factory),
    ],
) -> str | None:
    async with request.form() as form_data:
        user = UserLogin.model_validate(form_data)

    is_user = await user_service.get_user_by_email(
        email=user.email.lower(),
    )

    if is_user and bcrypt.checkpw(
        password=user.password.encode("utf-8"),
        hashed_password=is_user.hashed_password.encode("utf-8"),
    ):

        return await create_session(is_user)

    return None
