
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from core.models import Program


def get_all_programs(session: Session) -> list[Program]:
    """Возвращает все программы как объекты Program."""
    stmt = select(Program).order_by(Program.id)
    return list(session.scalars(stmt).all())


def get_program_by_name(session: Session, name: str) -> Program | None:
    stmt = select(Program).where(
        func.lower(Program.name) == name.lower(),
    )
    return session.scalars(stmt).first()


def create_program_in_db(
    session: Session,
    program: Program,
) -> Program:
    session.add(program)
    session.commit()
    return program


def delete_program_from_db(session: Session, name: str) -> None:
    stmt = delete(Program).where(func.lower(Program.name) == name.lower())
    session.execute(stmt)
    session.commit()
