from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from core.models import db_helper
from dependencies.auth.common import admin_basic_auth, raise_auth_error
from services.auth.admin_service import validate_admin


def admin_auth_dependency(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(admin_basic_auth),
    ],
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> None:
    if validate_admin(
        session=session,
        username=credentials.username,
        password=credentials.password,
    ):
        return

    raise_auth_error()
