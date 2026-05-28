import uuid

from aiopath import AsyncPath
from fastapi import Request, UploadFile
from sqladmin import ModelView
from wtforms import FileField

from core.config import settings
from core.models import Program
from utils.file_size import get_file_size


class ProgramAdmin(ModelView, model=Program):
    column_list = [
        Program.id,
        Program.name,
        Program.description,
        Program.file_size,
        Program.folder_path,
        Program.author,
    ]

    form_columns = [
        Program.name,
        Program.description,
        Program.author,
        Program.folder_path,
    ]

    form_overrides = {
        "folder_path": FileField,
    }

    can_edit = False

    async def on_model_change(
        self,
        data: dict[str, str | UploadFile],
        model: Program,
        is_created: bool,
        request: Request,
    ) -> None:

        file: UploadFile = data.get("folder_path")

        file_path = (
            settings.uploads_program_dir / f"{uuid.uuid4().hex}"
            f"{AsyncPath(file.filename).suffix}"
        )

        content = await file.read()

        async with file_path.open("wb") as buffer:
            await buffer.write(content)

        data.update(folder_path=str(file_path))
        data.update(file_size=await get_file_size(file_path))
