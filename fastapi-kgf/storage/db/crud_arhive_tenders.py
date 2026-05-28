from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ArchiveTender, Tender
from core.schemas.tenders import TenderCreate

from .base_crud import BaseCRUD


class ArchiveTendersStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ArchiveTender)

    async def add_all_from_active_tender(self, tenders: list[Tender]) -> None:
        archive_tenders = [
            ArchiveTender(**TenderCreate.model_validate(tender).model_dump())
            for tender in tenders
        ]

        self.session.add_all(archive_tenders)
        await self.session.commit()
