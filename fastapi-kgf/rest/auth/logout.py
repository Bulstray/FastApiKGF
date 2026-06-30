from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from services.auth.session_manager import delete_session

from core.config import settings

router = APIRouter(prefix=settings.api.v1.logout)


@router.get(
    "/",
    name="auth:logout",
    response_model=None,
)
async def logout_page(
    _: Annotated[
        None,
        Depends(delete_session),
    ],
) -> RedirectResponse:

    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )
