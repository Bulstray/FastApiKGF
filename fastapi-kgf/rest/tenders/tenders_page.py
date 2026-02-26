from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from core.schemas.user import UserRead
from dependencies.session_auth import require_auth
from templating.jinja_template import templates

router = APIRouter()


@router.get("/", name="tenders:page")
def tenders_page(
    request: Request,
    is_authenticated: Annotated[
        UserRead,
        Depends(
            require_auth,
        ),
    ],
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context={
            "tenders": [],
            "is_authenticated": is_authenticated,
        },
    )
