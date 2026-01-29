import shutil
from pathlib import Path

from fastapi import UploadFile

from core.config import settings
from utils.file_size import get_file_size


class ProgramFilesService:
    def __init__(self) -> None:
        self.upload_path = settings.uploads_program_dir

    def save_program_file(self, file: UploadFile) -> Path:

        if not file.filename:
            msg = "File must have a filename"
            raise ValueError(msg)

        file_path = self.upload_path / file.filename

        if file_path.exists():
            msg = f"File {file.filename} already exists"
            raise FileExistsError(msg)

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

    @staticmethod
    def delete_program_file(file: Path) -> None:
        if file.exists():
            file.unlink()

    @staticmethod
    def get_file_size_kb(file_path: Path) -> str:
        return get_file_size(file_path)
