from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies.session_auth import get_authenticated_user
from templating.jinja_template import templates

router = APIRouter()


@router.get("/", name="home")
def home(
    request: Request,
    is_authenticated: Annotated[
        UserRead,
        Depends(get_authenticated_user),
    ],
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"is_authenticated": is_authenticated},
    )
