from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import RedirectResponse

from services.auth.session_manager import delete_session

router = APIRouter(prefix="/logout")


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
