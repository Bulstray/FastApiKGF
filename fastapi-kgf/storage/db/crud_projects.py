from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import Project
from core.schemas.projects import ProjectCreate, ProjectRead


async def get_projects(session: AsyncSession) -> list[Project]:
    stmt = select(Project).order_by(Project.id)
    result = await session.scalars(stmt)
    return list(result.all())


async def create_project(
    session: AsyncSession, project_in: ProjectCreate
) -> ProjectRead:
    project = Project(**project_in.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectRead.model_validate(project)


async def get_project_by_id(
    session: AsyncSession,
    project_id: int,
) -> Project | None:
    return await session.get(Project, project_id)


async def delete_project(session: AsyncSession, project_id: int) -> None:
    # Находим проект по id
    project = await session.get(Project, project_id)

    if project:
        await session.delete(project)
        await session.commit()
