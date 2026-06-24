from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from core.models import ParsingKeyword

from .base_crud import BaseCRUD


async def get_all_keywords_tender(
    session: AsyncSession,
) -> list[ParsingKeyword]:
    stmt = select(ParsingKeyword).order_by(ParsingKeyword.id)
    result = await session.scalars(stmt)
    return list(result.all())


class KeyWordTendersStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, model=ParsingKeyword)
