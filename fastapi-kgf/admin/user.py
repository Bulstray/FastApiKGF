from typing import Any

from sqladmin import ModelView
from core.models import User
from dependencies.session_auth import get_authenticated_user
from core.types import UserRole

from utils.password_service import hash_password

from fastapi import Request

FIELD_USER = [
    User.username,
    User.email,
    User.name,
    User.surname,
    User.hashed_password,
    User.role,
]


async def auth_admin(request: Request) -> bool:
    user = await get_authenticated_user(request=request)
    if user is None:
        return False

    return user.role == UserRole.admin


class UserAdmin(ModelView, model=User):
    column_list = FIELD_USER
    form_columns = FIELD_USER
    column_details_list = FIELD_USER

    async def on_model_change(
        self,
        data: dict,
        model: Any,
        is_created: bool,
        request: Request,
    ) -> None:
        raw_password = data.get("hashed_password")
        if is_created or raw_password != model.hashed_password:
            data.update(hashed_password=hash_password(raw_password))
