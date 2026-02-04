from typing import Annotated

from fastapi import APIRouter, Query
from starlette.requests import Request
from starlette.responses import HTMLResponse

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


@router.get("/tenders_search", name="tenders:search")
def tenders_search(
    request: Request,
    search: Annotated[str, Query()],
) -> HTMLResponse:
    tender_data = TenderParseCore(key_word=search)
    context = {
        "tenders": tender_data.search_all_platforms(),
    }
    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context=context,
    )
