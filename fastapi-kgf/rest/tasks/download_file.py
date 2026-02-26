from typing import Annotated

from fastapi import Depends, APIRouter, Request
from starlette.responses import FileResponse

from core.schemas.user import UserRead
from dependencies.session_auth import require_auth


router = APIRouter(prefix="/download")


@router.get("/{name}/{file_path:path}", name="tasks:download")
async def download_file(
    name: str,
    file_path: str,
    is_auth_user: Annotated[UserRead, Depends(require_auth)],
    request: Request,
):
    return FileResponse(
        file_path,
        filename=name,
    )
