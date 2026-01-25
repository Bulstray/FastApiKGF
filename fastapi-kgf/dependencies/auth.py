from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status

from typing import Annotated

from sqlalchemy.orm import Session

from services.auth.db_user_helper import validate_user_password
from core.models import db_helper


user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username and password",
    auto_error=True,
)


def validate_basic_auth(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(user_basic_auth),
    ],
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
):
    if credentials and validate_user_password(
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
