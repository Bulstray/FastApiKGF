from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from core.schemas.user import UserRead
from dependencies.session_auth import require_auth
from services.tenders import service as tenders_service
from templating.jinja_template import templates

router = APIRouter(
    prefix="/tenders",
)


@router.get("/", name="tenders:page")
def tenders_page(
    request: Request,
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context={"tenders": []},
    )


@router.get(
    "/tenders_search",
    name="tenders:search",
    response_model=None,
)
def tenders_search(
    request: Request,
    search: Annotated[str, Query()],
    user: Annotated[UserRead, Depends(require_auth)],
) -> HTMLResponse | RedirectResponse:

    context = {
        "tenders": tenders_service.get_tenders_by_keyword(
            keyword=search,
        ),
    }
    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context=context,
    )
