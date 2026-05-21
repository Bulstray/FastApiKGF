from sqlalchemy.ext.asyncio.session import AsyncSession

from core.models import ParsingKeyword

from .base_crud import BaseCRUD


class KeyWordTendersStorage(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=ParsingKeyword)
