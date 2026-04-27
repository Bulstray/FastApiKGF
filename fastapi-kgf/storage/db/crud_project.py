from .base_crud import BaseCRUD

from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Project


class ProjectStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Project)
