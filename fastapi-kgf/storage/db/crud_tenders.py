from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.tenders import TenderCreate as TenderSchema

from core.models import Tender


async def get_all_active_tenders(
    session: AsyncSession,
) -> list[Tender]:
    stmt = select(Tender).order_by(Tender.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def clear_table(session: AsyncSession) -> None:
    stmt = delete(Tender)
    await session.execute(stmt)
    await session.commit()


async def add_tenders_in_db(
    session: AsyncSession,
    tenders: list[TenderSchema],
) -> None:
    tenders_models = [Tender(**tender.model_dump()) for tender in tenders]
    session.add_all(tenders_models)
    await session.commit()
