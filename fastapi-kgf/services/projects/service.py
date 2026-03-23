from sqlalchemy.ext.asyncio import AsyncSession

from starlette.datastructures import FormData

from storage.db import crud_projects
from core.schemas.projects import ProjectCreate


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_projects(self):
        return await crud_projects.get_projects(self.session)

    async def create_project(self, form_data: FormData):
        project_in = ProjectCreate.model_validate(form_data)

        return await crud_projects.create_project(
            self.session,
            project_in,
        )

    async def get_project_by_id(self, project_id: int):
        return await crud_projects.get_project_by_id(
            self.session,
            project_id,
        )

    async def delete_project(self, project_id: int):
        await crud_projects.delete_project(self.session, project_id)
