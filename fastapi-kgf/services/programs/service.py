from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.models import Program
from core.schemas import ProgramCreate
from crud.program_exceptions import (
    ProgramFileNameAlreadyExistsError,
    ProgramNameAlreadyExistsError,
    ProgramNameDoesNotExistError,
)
from crud.programs import (
    create_program_in_db,
    delete_program_from_db,
)
from crud.programs import get_all_programs as crud_get_all_programs
from crud.programs import get_program_by_name as crud_get_program_by_name

from .files import ProgramFilesService


class ProgramService:
    def __init__(
        self,
        session: Session,
        file_service: ProgramFilesService,
    ) -> None:
        self.session = session
        self.file_service = file_service

    def get_all_programs(self) -> list[Program]:
        return crud_get_all_programs(self.session)

    def get_program_by_name(
        self,
        program_name: str,
    ) -> Program | None:
        return crud_get_program_by_name(self.session, program_name)

    def create_program(
        self,
        program_in: ProgramCreate,
        file: UploadFile,
    ) -> Program:
        if self.get_program_by_name(program_name=program_in.name):
            raise ProgramNameAlreadyExistsError(program_in.name)

        try:
            file_path = self.file_service.save_program_file(file)
        except FileExistsError as exc:
            raise ProgramFileNameAlreadyExistsError(file.filename) from exc

        program = Program(
            **program_in.model_dump(),
            folder_path=str(file_path),
            file_size=self.file_service.get_file_size_kb(
                file_path,
            ),
        )

        return create_program_in_db(self.session, program)

    def delete_program(self, name: str) -> None:
        program = self.get_program_by_name(
            program_name=name,
        )

        if not program:
            raise ProgramNameDoesNotExistError(name)

        file_path = Path(program.folder_path)

        self.file_service.delete_program_file(file_path)

        delete_program_from_db(
            session=self.session,
            name=name,
        )
