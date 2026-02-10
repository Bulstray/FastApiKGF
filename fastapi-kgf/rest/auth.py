import uuid

from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends,
    status,
    Response,
    Cookie,
    HTTPException,
)

from fastapi.responses import RedirectResponse
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.auth_user import validate_basic_auth_user

from templating.jinja_template import templates
from core.models import db_helper

from time import time
from core.config.settings import COOKIES, COOKIES_SESSION_ID_KEY

router = APIRouter(
    prefix="/login",
)


@router.get("/", name="login:get")
def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request,
    )


@router.get("/logout", name="login:logout")
def logout_page(request: Request, return_url: str | None = None):
    redirect = RedirectResponse(
        url=return_url or "/",
        status_code=status.HTTP_303_SEE_OTHER,
    )

    redirect.delete_cookie(COOKIES_SESSION_ID_KEY)
    return redirect


def get_session_data(
    session_id: str = Cookie(
        alias=COOKIES_SESSION_ID_KEY,
    ),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session id",
        )
    return COOKIES[session_id]


@router.post("/", name="login:post")
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
    if not user:
        return templates.TemplateResponse(
            name="login.html",
            request=request,
            context={"error": "Неверный логин или пароль"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    redirect = RedirectResponse(
        url=request.url_for("home"),
        status_code=status.HTTP_303_SEE_OTHER,
    )

    session_id = uuid.uuid4().hex

    COOKIES[session_id] = {
        "username": user.username,
        "loging_at": int(time()),
    }

    redirect.set_cookie(key=COOKIES_SESSION_ID_KEY, value=session_id)

    return redirect
