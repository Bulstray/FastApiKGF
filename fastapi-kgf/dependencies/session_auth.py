from typing import Annotated

from fastapi import Depends, HTTPException, status, Request, Cookie
from fastapi.responses import HTMLResponse
from fastapi.security import APIKeyCookie
from starlette.websockets import WebSocket

from core.config.settings import SESSION_COOKIE_NAME
from core.schemas.user import UserRead
from storage.redis import session
from core.schemas.cookie import Cookies

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


async def get_cookie_websocket(
    websocket: WebSocket, session_id: Annotated[Cookies, Cookie()]
):
    if session_id and (
        answer := await session.get_by_session_id(session_id.web_app_session_id)
    ):
        return answer

    raise HTTPException(
        status_code=status.HTTP_303_SEE_OTHER,
        headers={"Location": "/login"},
    )


async def require_auth(
    user: Annotated[None | UserRead, Depends(get_authenticated_user)],
) -> UserRead:
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
