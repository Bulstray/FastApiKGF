from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Program

from .base_crud import BaseCRUD


class ProgramsStorage(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Program)
