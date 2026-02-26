import base64
import uuid

from aiopath import AsyncPath
from fastapi import UploadFile

from utils.file_size import get_file_size


class FilesService:
    def __init__(self, uploads_path: AsyncPath) -> None:
        self.upload_path: AsyncPath = uploads_path

    async def save_program_file(self, file: UploadFile, content: bytes) -> AsyncPath:

        if not file.filename:
            msg = "File must have a filename"
            raise ValueError(msg)

        file_path = (
            self.upload_path / f"{uuid.uuid4().hex}{AsyncPath(file.filename).suffix}"
        )

        async with file_path.open("wb") as buffer:
            await buffer.write(content)

        return file_path

    async def save_program_file_bs64(self, code_file: str, filename: str) -> AsyncPath:
        content = code_file.split(";base64,")[-1]

        file_path = self.upload_path / f"{uuid.uuid4().hex}{AsyncPath(filename).suffix}"

        async with file_path.open("wb") as file_ctx:
            await file_ctx.write(base64.b64decode(content))

        return file_path

    @staticmethod
    async def get_file_size_kb(file_path: AsyncPath) -> str:
        return await get_file_size(file_path)
