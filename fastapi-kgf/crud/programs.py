import shutil
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import UploadFile

from core.models import Program
from core.schemas import ProgramCreate

from core.config import BASE_UPLOADS_PROGRAMS


def get_all_programs(
    session: Session,
) -> Sequence[Program]:
    stmt = select(Program.name, Program.description).order_by(Program.id)
    result = session.scalars(stmt)
    return result.all()


def create_program(
    session: Session,
    program_create: ProgramCreate,
    file: UploadFile,
) -> None:
    folder_path = BASE_UPLOADS_PROGRAMS / file.filename

    program = Program(
        name=program.name,
        description=program.description,
        folder_path=folder_path,
    )

    with Path(folder_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    session.add(program)
    session.commit()
