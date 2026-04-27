from sqlalchemy.ext.asyncio import AsyncSession

from starlette.datastructures import FormData

from core.schemas.projects import ProjectCreate, ProjectRead
from core.models import Project
from storage.db.base_crud import BaseCRUD


class ProjectService(BaseCRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Project)

    async def create_project(self, form_data: FormData) -> ProjectRead:
        project_in = ProjectCreate.model_validate(form_data)
        project_in = await self.create(
            Project(
                **project_in.model_dump(),
            )
        )
        return ProjectRead.model_validate(project_in)
