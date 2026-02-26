from typing import Annotated

from fastapi import Query, Depends, APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from core.schemas.user import UserRead
from dependencies.session_auth import require_auth
from services.tenders import service as tenders_service
from templating.jinja_template import templates

router = APIRouter(prefix="/tenders_search")


@router.get(
    "/",
    name="tenders:search",
    response_model=None,
)
def tenders_search(
    request: Request,
    search: Annotated[str, Query()],
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
