from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from core.config.settings import SESSION_COOKIE_NAME
from core.schemas.user import UserRead
from storage.redis.session import SessionStorage


def get_authenticated_user(
    request: Request,
) -> UserRead | None:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)

    if session_id is None:
        return None

    if (answer := SessionStorage.get_by_session_id(session_id)) is not None:
        return answer

    return None


def require_auth(
    user: Annotated[UserRead | None, Depends(get_authenticated_user)],
) -> UserRead | HTMLResponse:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )

    return user


def redirect_if_authenticated(
    user: Annotated[UserRead | None, Depends(get_authenticated_user)],
) -> UserRead | None:
    if user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )

    return user
