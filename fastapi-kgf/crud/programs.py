import shutil
from collections.abc import Sequence

from fastapi import UploadFile
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from core.config import BASE_UPLOADS_PROGRAMS
from core.models import Program
from core.schemas import ProgramCreate


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

    folder_path = BASE_UPLOADS_PROGRAMS / str(file.filename)

    program = Program(
        name=program_create.name,
        description=program_create.description,
        folder_path=str(folder_path),
    )

    with folder_path.open(mode="wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    session.add(program)
    session.commit()


def delete_program(session: Session, program_id: int) -> None:
    stmt = delete(Program).where(Program.id == program_id)
    session.execute(stmt)
    session.commit()
