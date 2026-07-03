from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.schemas import UserRead
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates
from storage.db import crud_project
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

from storage.db import crud_user_settings

from core.schemas import UserSettings

router = APIRouter(prefix="/settings")


@router.get("/", name="settings:page")
async def settings_page(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse:

    return templates.TemplateResponse(
        "settings.html",
        context={
            "user": current_user,
            "request": request,
            "projects": await crud_project.get_all_projects(session),
            "settings": await crud_user_settings.get_settings_by_user(
                session,
                current_user.id,
            ),
        },
    )


@router.post(
    "/",
    name="settings:update",
    status_code=status.HTTP_303_SEE_OTHER,
)
async def update_settings(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> HTMLResponse:
    async with request.form() as form_data:
        settings_schema = UserSettings.model_validate(form_data)

        user_settings = await crud_user_settings.get_settings_by_user(
            session,
            current_user.id,
        )

        if user_settings:
            await crud_user_settings.update_settings(
                session,
                current_user.id,
                settings_schema,
            )
        else:
            await crud_user_settings.create_user_settings(
                session,
                current_user.id,
                settings_schema,
            )

    return templates.TemplateResponse(
        "settings.html",
        context={
            "user": current_user,
            "request": request,
            "projects": await crud_project.get_all_projects(session),
            "settings": await crud_user_settings.get_settings_by_user(
                session,
                current_user.id,
            ),
            "success": "Настройки успешно сохраненны",
        },
    )
