from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.config.settings import SESSION_COOKIE_NAME
from dependencies.auth_user import validate_basic_auth_user
from templating.jinja_template import templates

router = APIRouter()


@router.post(
    "/",
    name="login:post",
    response_model=None,
)
async def login_submit(
    request: Request,
    session_id: Annotated[
        str | None,
        Depends(validate_basic_auth_user),
    ],
) -> HTMLResponse | RedirectResponse:

    if session_id is None:
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
