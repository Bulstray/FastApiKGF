import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from fastapi import UploadFile
from sqlalchemy import Row, delete, func, select
from sqlalchemy.orm import Session

from core.config import BASE_UPLOADS_PROGRAMS
from core.models import Program
from core.schemas import ProgramCreate
from utils import get_file_size

from .program_exceptions import (
    ProgramFileNameAlreadyExistsError,
    ProgramNameAlreadyExistsError,
    ProgramNameDoesNotExistError,
)


def get_all_programs(
    session: Session,
) -> Sequence[Row[tuple[Any, Any, Any]]]:
    """

    :rtype: object
    """
    stmt = select(
        Program.name,
        Program.description,
        Program.file_size,
    ).order_by(
        Program.id,
    )
    result = session.execute(stmt)
    return result.all()


def get_file_by_name(session: Session, name: str) -> Row[tuple[str]] | None:
    stmt = select(Program.folder_path).where(
        func.lower(Program.name) == name.lower(),
    )
    result = session.execute(stmt)
    return result.first()


def create_program(
    session: Session,
    program_create: ProgramCreate,
    file: UploadFile,
) -> None:
    folder_path = BASE_UPLOADS_PROGRAMS / str(file.filename)

    if folder_path.exists():
        raise ProgramFileNameAlreadyExistsError(folder_path)

    if get_file_by_name(session=session, name=program_create.name) is not None:
        raise ProgramNameAlreadyExistsError(program_create.name)

    with folder_path.open(mode="wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    program = Program(
        name=program_create.name,
        description=program_create.description,
        folder_path=str(folder_path),
        file_size=get_file_size(folder_path),
    )

    session.add(program)
    session.commit()


def delete_program(session: Session, name: str) -> None:
    result = get_file_by_name(session, name=name)

    if result is None:
        raise ProgramNameDoesNotExistError(name)

    folder_path_str = result[0]
    Path(folder_path_str).unlink()

    stmt = delete(Program).where(func.lower(Program.name) == name.lower())
    session.execute(stmt)
    session.commit()
