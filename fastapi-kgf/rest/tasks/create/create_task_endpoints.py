from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from dependencies import TaskFactory
from storage.db import crud_project

from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/{project_id}",
    name="tasks:post",
    response_class=RedirectResponse,
    status_code=status.HTTP_303_SEE_OTHER,
)
async def create_task(
    request: Request,
    project_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    service: Annotated[
        TaskFactory,
        Depends(TaskFactory),
    ],
) -> str:

    project = await crud_project.get_project_by_id(
        session,
        project_id,
    )
    if project is None:
        return "/"

    async with request.form() as form:
        content = await form.get("rar_file").read()

        await service.create_task(
            form=form,
            content=content,
        )

    return f"/projects/{project_id}"
