from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.config.settings import SESSION_COOKIE_NAME
from core.schemas.user import UserRead
from dependencies.session_auth import require_auth
from services.auth.session_manager import SessionManager

router = APIRouter(prefix="/logout")


@router.get(
    "/logout",
    name="auth:logout",
    response_model=None,
)
async def logout_page(
    request: Request,
    user: Annotated[UserRead, Depends(require_auth)],
    return_url: str | None = None,
) -> HTMLResponse | RedirectResponse:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)

    if session_id:
        session_service = SessionManager()
        session_service.delete_session(session_id)

    redirect = RedirectResponse(
        url=return_url or "/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.delete_cookie(SESSION_COOKIE_NAME)
    return redirect
