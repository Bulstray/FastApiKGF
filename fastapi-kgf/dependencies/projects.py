from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.projects.service import ProjectService
from services.users.service import UserService

from dependencies.providers import get_user_service

from storage.db.crud_user import get_all_users

from core.models import db_helper

from typing import Annotated


async def get_project_service(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> ProjectService:
    return ProjectService(session)