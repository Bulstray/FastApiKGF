from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import ArchiveTender, Tender
from core.schemas.tenders import TenderCreate


async def add_all_from_active_tender(
    session: AsyncSession,
    tenders: list[Tender],
) -> None:
    archive_tenders = [
        ArchiveTender(**TenderCreate.model_validate(tender).model_dump())
        for tender in tenders
    ]

    session.add_all(archive_tenders)
    await session.commit()


async def delete_archive_tender(
    session: AsyncSession,
    archive_tender: ArchiveTender,
) -> None:
    await session.delete(archive_tender)
    await session.commit()


async def get_archive_tender_by_url(
    session: AsyncSession,
    url: str,
) -> ArchiveTender | None:
    stmt = select(ArchiveTender).where(ArchiveTender.url == url)
    result = await session.scalars(stmt)
    return result.first()
