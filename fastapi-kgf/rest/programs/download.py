from typing import Annotated

from aiopath import AsyncPath
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, RedirectResponse

from dependencies.programs.programs import ProgramsFactory

router = APIRouter()


@router.get(
    "/{_id}/download",
    name="program:download",
    response_model=None,
)
async def download_program(
    program_service: Annotated[
        ProgramsFactory,
        Depends(ProgramsFactory),
    ],
    _id: int,
) -> RedirectResponse | FileResponse:

    program = await program_service.get_by_id(_id)

    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found",
        )

    file_path = AsyncPath(program.folder_path)

    if not await file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in server",
        )

    try:
        file_response = FileResponse(
            str(file_path),
            filename=file_path.name,
        )
    except Exception:
        file_response = FileResponse(str(file_path))

    return file_response
