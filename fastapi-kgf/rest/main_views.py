from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from templating.jinja_template import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
def home_page(
    request: Request,
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="home_page.html",
    )
