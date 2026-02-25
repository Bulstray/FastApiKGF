import uuid

from aiopath import AsyncPath
from fastapi import UploadFile

from utils.file_size import get_file_size


class FilesService:
    def __init__(self, uploads_path: AsyncPath) -> None:
        self.upload_path: AsyncPath = uploads_path

    async def save_program_file(self, file: UploadFile) -> AsyncPath:

        if not file.filename:
            msg = "File must have a filename"
            raise ValueError(msg)

        file_path = (
            self.upload_path / f"{uuid.uuid4().hex}{AsyncPath(file.filename).suffix}"
        )

        if await file_path.exists():
            msg = f"File {file.filename} already exists"
            raise FileExistsError(msg)

        async with file_path.open("wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        return file_path

    @staticmethod
    async def delete_program_file(file: AsyncPath) -> None:
        if await file.exists():
            await file.unlink()

    @staticmethod
    async def get_file_size_kb(file_path: AsyncPath) -> str:
        return await get_file_size(file_path)
