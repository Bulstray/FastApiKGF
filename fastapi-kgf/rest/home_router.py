from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from templating.jinja_template import templates


router = APIRouter()


@router.get("/", name="home")
def home(
    request: Request,
) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )
