from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from core.models import ArchiveTender

from .base_crud import BaseCRUD


class ArchiveTendersStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ArchiveTender)

    async def add_all(self, tenders: list[ArchiveTender]) -> None:
        self.session.add_all(tenders)
        await self.session.commit()
