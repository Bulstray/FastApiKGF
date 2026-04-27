from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(prefix="/download")


@router.get("/{name}/{file_path:path}", name="tasks:download")
async def download_file(
    name: str,
    file_path: str,
) -> FileResponse:
    return FileResponse(
        file_path,
        filename=name,
    )
