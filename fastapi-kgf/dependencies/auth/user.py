from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from core.models import db_helper
from dependencies.auth.common import raise_auth_error, user_basic_auth
from services.auth.auth_service import authenticate_user


def validate_basic_auth(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(user_basic_auth),
    ],
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> None:
    if authenticate_user(
        session=session,
        password=credentials.password,
        username=credentials.username,
    ):
        return

    raise_auth_error()
