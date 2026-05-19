from typing import Any

from fastapi import Request
from sqladmin import ModelView

from core.models import User
from utils.password_service import hash_password

FIELD_USER = [
    User.email,
    User.name,
    User.surname,
    User.hashed_password,
    User.role,
]


class UserAdmin(ModelView, model=User):
    column_list = FIELD_USER
    form_columns = FIELD_USER
    column_details_list = FIELD_USER

    async def on_model_change(
        self,
        data: dict[str, Any],
        model: Any,
        is_created: bool,
        request: Request,
    ) -> None:
        raw_password = data.get("hashed_password")
        if (
            raw_password is not None
            and isinstance(raw_password, str)
            and (is_created or raw_password != model.hashed_password)
        ):
            data.update(hashed_password=hash_password(raw_password))
