from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyCookie

from core.config.settings import SESSION_COOKIE_NAME
from core.schemas.user import UserRead
from storage.redis import session


cookie_scheme = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)


async def get_authenticated_user(
    request: Request,
    session_id: Annotated[
        str | None,
        Depends(cookie_scheme),
    ],
) -> UserRead | None:
    if session_id and (answer := await session.get_by_session_id(session_id)):
        return answer

    return None


async def get_current_user(
    session_id: Annotated[
        str,
        Depends(cookie_scheme),
    ],
) -> UserRead:
    return await session.get_by_session_id(session_id)


async def get_cookie_for_websocket(
    websocket: WebSocket, session_id: Annotated[str | None, Cookie()]
):
    print(session_id)


async def require_auth(
    user: Annotated[UserRead | None, Depends(get_authenticated_user)],
) -> UserRead | HTMLResponse:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )

    return user


async def redirect_if_authenticated(
    user: Annotated[UserRead | None, Depends(get_authenticated_user)],
) -> UserRead | None:
    if user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )

    return user
