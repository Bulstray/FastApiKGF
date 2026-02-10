from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Program
from typing import cast


async def get_all_programs(session: AsyncSession) -> list[Program]:
    """Возвращает все программы как объекты Program."""
    stmt = select(Program).order_by(Program.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_program_by_name(
    session: AsyncSession,
    name: str,
) -> Program | None:
    stmt = select(Program).where(
        func.lower(Program.name) == name.lower(),
    )
    result = await session.scalars(stmt)
    return result.first()


async def create_program_in_db(
    session: AsyncSession,
    program: Program,
) -> Program:
    session.add(program)
    await session.commit()
    await session.refresh(program)
    return program


async def delete_program_from_db(session: AsyncSession, name: str) -> None:
    stmt = delete(Program).where(func.lower(Program.name) == name.lower())
    await session.execute(stmt)
    await session.commit()
