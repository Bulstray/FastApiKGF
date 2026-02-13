from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Form,
    Request,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import SESSION_COOKIE_NAME
from core.models import db_helper
from core.schemas.user import UserRead
from dependencies.auth_user import validate_basic_auth_user
from dependencies.session_auth import redirect_if_authenticated, require_auth
from services.auth.session_manager import SessionManager
from templating.jinja_template import templates

router = APIRouter(
    prefix="/login",
)


@router.get("/", name="login:get")
async def login_page(
    request: Request,
    user: Annotated[
        UserRead,
        Depends(redirect_if_authenticated),
    ],
) -> HTMLResponse:
    return templates.TemplateResponse(
        name="login.html",
        request=request,
    )


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


@router.post(
    "/",
    name="login:post",
    response_model=None,
)
async def login_submit(
    request: Request,
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse | RedirectResponse:
    user = await validate_basic_auth_user(
        username=username,
        password=password,
        session=session,
    )

    if user is None:
        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={"error": "Неверный логин или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    session_id = SessionManager.create_session(user=user)

    redirect = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.set_cookie(key=SESSION_COOKIE_NAME, value=session_id)

    return redirect
