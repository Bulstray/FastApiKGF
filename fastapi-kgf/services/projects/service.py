from sqlalchemy.ext.asyncio import AsyncSession

from storage.db.crud_project import ProjectStorage


class ProjectService(ProjectStorage):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
