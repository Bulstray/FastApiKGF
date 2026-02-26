from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Request
from starlette.responses import FileResponse

from dependencies.session_auth import require_auth

if TYPE_CHECKING:
    from core.schemas.user import UserRead

router = APIRouter(prefix="/download")


@router.get("/{name}/{file_path:path}", name="tasks:download")
async def download_file(
    name: str,
    file_path: str,
    is_auth_user: Annotated["UserRead", Depends(require_auth)],
    request: Request,
) -> FileResponse:
    return FileResponse(
        file_path,
        filename=name,
    )
