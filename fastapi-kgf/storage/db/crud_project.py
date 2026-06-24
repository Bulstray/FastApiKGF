from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import Project

from .base_crud import BaseCRUD


async def get_all_projects(session: AsyncSession) -> list[Project]:
    stmt = select(Project).order_by(Project.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def get_project_by_id(
    session: AsyncSession,
    project_id: int,
) -> Project | None:
    return await session.get(Project, project_id)


class ProjectStorage(BaseCRUD):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Project)
