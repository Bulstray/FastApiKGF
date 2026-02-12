from typing import Annotated

from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Form,
    Request,
    status,
)
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import SESSION_COOKIE_NAME
from core.models import db_helper
from dependencies.auth_user import validate_basic_auth_user
from dependencies.session_auth import require_auth, redirect_if_authenticated
from services.auth.session_manager import SessionManager
from templating.jinja_template import templates

router = APIRouter(
    prefix="/login",
)


@router.get("/", name="login:get")
async def login_page(
    request: Request,
    user: Annotated[
        dict,
        Depends(redirect_if_authenticated),
    ],
):
    return templates.TemplateResponse(
        name="login.html",
        request=request,
    )


@router.get("/logout", name="auth:logout")
async def logout_page(
    request: Request,
    user: Annotated[dict, Depends(require_auth)],
    return_url: str | None = None,
    session_id: str | None = Cookie(alias=SESSION_COOKIE_NAME),
):

    if session_id:
        session_service = SessionManager()
        session_service.delete_session(session_id, request=request)

    redirect = RedirectResponse(
        url=return_url or "/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.delete_cookie(SESSION_COOKIE_NAME)
    return redirect


@router.post(
    "/",
    name="login:post",
)
async def login_submit(
    request: Request,
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    user = await validate_basic_auth_user(
        username=username,
        password=password,
        session=session,
    )

    session_id = SessionManager.create_session(user=user)

    if not user:
        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={"error": "Неверный логин или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    redirect = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.set_cookie(key=SESSION_COOKIE_NAME, value=session_id)

    return redirect
