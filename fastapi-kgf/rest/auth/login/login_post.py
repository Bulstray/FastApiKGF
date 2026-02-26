from typing import Annotated

from fastapi import Form, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.config.settings import SESSION_COOKIE_NAME
from core.models import db_helper
from dependencies.auth_user import validate_basic_auth_user
from services.auth.session_manager import SessionManager
from templating.jinja_template import templates

router = APIRouter()


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

    session_id = await SessionManager.create_session(user=user)

    redirect = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.set_cookie(key=SESSION_COOKIE_NAME, value=session_id)

    return redirect
