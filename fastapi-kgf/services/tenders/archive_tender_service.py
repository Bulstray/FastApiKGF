from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ArchiveTender, Tender
from core.schemas.tenders import TenderCreate as TenderSchema
from storage.db.crud_arhive_tenders import ArchiveTendersStorage


class ArchiveTendersService(ArchiveTendersStorage):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_tenders_in_db(self, tenders: list[Tender]) -> None:
        tenders_models = [
            ArchiveTender(**TenderSchema.model_validate(tender))
            for tender in tenders
        ]
        await self.add_all(tenders_models)
