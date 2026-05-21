from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ArchiveTender, Tender

from .base_crud import BaseCRUD


class TendersStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tender)

    async def add_all(self, tenders: list[Tender]) -> None:
        self.session.add_all(tenders)
        await self.session.commit()

    async def delete_table(self):
        stmt = delete(Tender)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_archive_tender(self, url: str) -> ArchiveTender | None:
        stmt = select(ArchiveTender).where(ArchiveTender.url == url)
        result = await self.session.scalars(stmt)
        return result.first()
