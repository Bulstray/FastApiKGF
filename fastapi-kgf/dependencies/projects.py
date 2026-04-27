from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services.projects.service import ProjectService


async def get_project_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ProjectService:
    return ProjectService(session)
