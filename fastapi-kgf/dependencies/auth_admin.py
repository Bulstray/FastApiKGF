from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status

from typing import Annotated

from sqlalchemy.orm import Session

from services.auth.db_admin_helper import validate_admin_password
from core.models import db_helper


admin_basic_auth = HTTPBasic(
    scheme_name="Basic Auth Admin",
    description="Basic username and password",
    auto_error=True,
)


def validate_basic_auth_admin(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(admin_basic_auth),
    ],
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
):
    if credentials and validate_admin_password(
        session=session,
        password=credentials.password,
        username=credentials.username,
    ):
        return None

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
