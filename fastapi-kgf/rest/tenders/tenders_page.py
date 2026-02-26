from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from templating.jinja_template import templates

router = APIRouter()


@router.get("/", name="tenders:page")
def tenders_page(
    request: Request,
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="tenders.html",
        context={"tenders": []},
    )
