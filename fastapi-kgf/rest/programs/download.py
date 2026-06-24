from typing import Annotated

from aiopath import AsyncPath
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, RedirectResponse

from storage.db import crud_programs
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

router = APIRouter()


@router.get(
    "/download/{_id}/",
    name="program:download",
    response_model=None,
)
async def download_program(
    _id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> RedirectResponse | FileResponse:

    program = await crud_programs.get_program_by_id(session, _id)

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

    return FileResponse(
        str(file_path),
        filename=file_path.name,
    )
