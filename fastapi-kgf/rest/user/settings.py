from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from core.schemas import UserRead
from dependencies import ProjectFactory, UserSettingsServiceFactory
from dependencies.session_auth import get_current_user
from templating.jinja_template import templates

router = APIRouter(prefix="/settings")


@router.get("/", name="settings:page")
async def settings_page(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    project_service: Annotated[
        ProjectFactory,
        Depends(ProjectFactory),
    ],
    user_setting_factory: Annotated[
        UserSettingsServiceFactory,
        Depends(UserSettingsServiceFactory),
    ],
) -> HTMLResponse:
    projects = await project_service.get_all()
    settings = await user_setting_factory.get_settings_by_user(current_user.id)

    return templates.TemplateResponse(
        "settings.html",
        context={
            "user": current_user,
            "projects": projects,
            "request": request,
            "settings": settings,
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
