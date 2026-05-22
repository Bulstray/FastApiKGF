from sqlalchemy import delete, func, select

from core.models import Program
from .base_crud import BaseCRUD
from sqlalchemy.ext.asyncio import AsyncSession


class ProgramsStorage(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Program)
