from fastapi import APIRouter, Request

from templating.jinja_template import templates

router = APIRouter(
    prefix="/auth",
)


@router.get("/")
def auth(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request,
    )
