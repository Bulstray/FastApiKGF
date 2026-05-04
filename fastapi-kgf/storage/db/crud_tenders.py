from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Tender

from .base_crud import BaseCRUD


class TendersStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tender)

    async def add_all(self, tenders: list[Tender]) -> None:
        self.session.add_all(tenders)
        await self.session.commit()
