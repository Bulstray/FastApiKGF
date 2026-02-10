from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.auth import admin_helper

admin_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username and password auth",
    auto_error=False,
)


async def validate_basic_auth(
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(admin_basic_auth),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:
    if credentials and await admin_helper.validate_admin_password(
        username=credentials.username,
        password=credentials.password,
        session=session,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
