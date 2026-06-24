from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.schemas import UserRead
from dependencies import UserSettingsServiceFactory
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates
from storage.db import crud_project, crud_user_settings
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

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
    response_class=RedirectResponse,
    status_code=status.HTTP_303_SEE_OTHER,
)
async def update_settings(
    request: Request,
    user_setting_service: Annotated[
        UserSettingsServiceFactory,
        Depends(UserSettingsServiceFactory),
    ],
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
) -> str:
    async with request.form() as form_data:
        await user_setting_service.update_settings_service(
            current_user.id,
            form_data,
        )

    return "/users/settings"
