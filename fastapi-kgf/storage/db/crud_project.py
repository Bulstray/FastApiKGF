from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Project

from .base_crud import BaseCRUD


class ProjectStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Project)
