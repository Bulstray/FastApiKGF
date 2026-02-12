from typing import Annotated

from fastapi import APIRouter, Query, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies.session_auth import require_auth
from parsers.core import TenderParseCore
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
    user: Annotated[dict, Depends(require_auth)],
) -> HTMLResponse | RedirectResponse:

    tender_data = TenderParseCore(key_word=search)
    context = {
        "tenders": tender_data.search_all_platforms(),
    }
    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context=context,
    )
