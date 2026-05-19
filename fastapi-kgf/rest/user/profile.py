from fastapi import APIRouter, Depends, Request

from pydantic import ValidationError

from fastapi.responses import HTMLResponse
from typing import Annotated
from core.schemas import UserRead, UserUpdateForm
from dependencies.session_auth import get_current_user
from dependencies.projects import get_project_service
from services import ProjectService, UserService
from templating.jinja_template import templates
from dependencies.user import get_user_service
from core.config.settings import SESSION_COOKIE_NAME

router = APIRouter(prefix="/profile")


@router.get("/", name="profile:page")
async def profile_page(
    request: Request,
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    project_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
) -> HTMLResponse:
    projects = await project_service.get_all()

    return templates.TemplateResponse(
        "profile.html",
        context={
            "user": current_user,
            "projects": projects,
            "request": request,
        },
    )


@router.post("/", name='profile:update')
async def update_profile(
    request: Request,
    user_service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    project_service: Annotated[
        ProjectService,
        Depends(get_project_service),
    ],
):
    projects = await project_service.get_all()
    async with request.form() as form_data:

        try:
            user_update = UserUpdateForm.model_validate(form_data)

        except ValidationError:
            return templates.TemplateResponse(
                "profile.html",
                context={
                    "user": current_user,
                    "projects": projects,
                    "request": request,
                    "error": True,
                },
            )

        else:
            await user_service.update_user_data(
                user_update,
                current_user.id,
            )
            print(request.get(SESSION_COOKIE_NAME))

            return templates.TemplateResponse(
                "profile.html",
                context={
                    "user": current_user,
                    "projects": projects,
                    "request": request,
                },
            )
