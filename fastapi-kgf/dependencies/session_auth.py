from fastapi import Request, Depends, HTTPException, status

from core.config.settings import SESSION_COOKIE_NAME

from typing import Annotated

from storage.session.session import SessionStorage


def get_authenticated_user(
    request: Request,
) -> None | dict[str, str]:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)

    if session_id is None:
        return None

    if (answer := SessionStorage.get_by_session_id(session_id)) is not None:
        return answer

    return None


def require_auth(
    request: Request,
    user: Annotated[dict | None, Depends(get_authenticated_user)],
) -> dict:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )

    return user


def redirect_if_authenticated(
    request: Request,
    user: Annotated[dict | None, Depends(get_authenticated_user)],
) -> dict:
    if user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/"},
        )

    return user
