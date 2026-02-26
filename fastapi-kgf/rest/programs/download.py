from typing import Annotated

from aiopath import AsyncPath
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import FileResponse, RedirectResponse

from dependencies.providers import get_program_service
from dependencies.session_auth import require_auth
from services.programs import ProgramService

router = APIRouter()


@router.get(
    "/{name}/download",
    name="program:download",
    response_model=None,
)
async def download_program(
    program_service: Annotated[
        ProgramService,
        Depends(get_program_service),
    ],
    is_authenticated: Annotated[
        bool,
        Depends(require_auth),
    ],
    name: str,
) -> RedirectResponse | FileResponse:

    program = await program_service.get_program_by_name(program_name=name)

    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program {name} not found",
        )

    file_path = AsyncPath(program.folder_path)

    if not await file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in server",
        )

    return FileResponse(
        str(file_path),
        filename=file_path.name,
    )
