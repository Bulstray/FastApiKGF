from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Program

from .base_crud import BaseCRUD


async def get_all_programs(session: AsyncSession) -> list[Program]:
    stmt = select(Program).order_by(Program.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_program_by_id(
    session: AsyncSession,
    program_id: int,
) -> Program | None:
    return await session.get(Program, program_id)


class ProgramsStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Program)
