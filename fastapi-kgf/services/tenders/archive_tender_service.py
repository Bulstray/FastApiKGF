from sqlalchemy.ext.asyncio import AsyncSession

from storage.db.crud_arhive_tenders import ArchiveTendersStorage


class ArchiveTendersService(ArchiveTendersStorage):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
