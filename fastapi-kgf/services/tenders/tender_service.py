from storage.db.crud_tenders import TendersStorage

from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.tenders import TenderCreate as TenderSchema
from core.models import Tender


class TendersService(TendersStorage):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add_tenders_in_db(self, tenders: list[TenderSchema]) -> None:

        tenders_models = [Tender(**tender.model_dump()) for tender in tenders]
        await self.add_all(tenders_models)
