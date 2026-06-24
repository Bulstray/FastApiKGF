from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.settings import SESSION_COOKIE_NAME
from dependencies.auth_user import validate_basic_auth_user
from templating.jinja_template import templates

from core.models import db_helper

router = APIRouter()


@router.post(
    "/",
    name="login:post",
    response_model=None,
)
async def login_submit(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse | RedirectResponse:

    session_id = await validate_basic_auth_user(
        request,
        session,
    )

    if session_id is None:
        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={"error": "Неверная почта или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    redirect = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
    )

    return redirect
