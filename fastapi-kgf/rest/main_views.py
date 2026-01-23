from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.models import db_helper
from crud import programs as crud_programs
from templating.jinja_template import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
def home_page(
    request: Request,
    session: Annotated[
        Session,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse:
    context: dict[str, Any] = {}
    programs = crud_programs.get_all_programs(
        session=session,
    )

    context.update(
        programs=programs,
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )
