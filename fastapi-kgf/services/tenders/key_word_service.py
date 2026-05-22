from sqlalchemy.ext.asyncio import AsyncSession

from storage.db.crud_keyword_tenders import KeyWordTendersStorage


class KeyWordService(KeyWordTendersStorage):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
