from fastapi import APIRouter, Request, Depends

from templating.jinja_template import templates
from dependencies.session_auth import require_auth

from typing import Annotated
from core.schemas.user import UserRead


router = APIRouter(prefix="/tasks")


@router.get("/", name="tasks:page")
def tasks_page(
    request: Request,
    is_auth: Annotated[UserRead, Depends(require_auth)],
    executor: int,
):
    return templates.TemplateResponse(
        name="tasks.html",
        request=request,
    )
