from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies.session_auth import redirect_if_authenticated
from templating.jinja_template import templates

router = APIRouter()


@router.get("/", name="login:get")
async def login_page(
    request: Request,
    is_auth: Annotated[
        UserRead,
        Depends(redirect_if_authenticated),
    ],
) -> HTMLResponse:
    return templates.TemplateResponse(
        name="login.html",
        request=request,
    )
