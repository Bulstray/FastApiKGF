from fastapi import APIRouter, Depends, Request

from pydantic import ValidationError

from fastapi.responses import HTMLResponse
from typing import Annotated
from storage.redis.session import save_session
from core.schemas import UserRead, UserUpdateForm
from dependencies.session_auth import get_current_user
from dependencies import ProjectFactory
from templating.jinja_template import templates
from dependencies.user import UserServiceFactory
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
        ProjectFactory,
        Depends(ProjectFactory),
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
        UserServiceFactory,
        Depends(UserServiceFactory),
    ],
    current_user: Annotated[
        UserRead,
        Depends(get_current_user),
    ],
    project_service: Annotated[
        ProjectFactory,
        Depends(ProjectFactory),
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

            session_id = request.cookies.get(SESSION_COOKIE_NAME)

            if user_update.email:
                current_user.email = user_update.email
                await save_session(session_id, current_user)

            return templates.TemplateResponse(
                "profile.html",
                context={
                    "user": current_user,
                    "projects": projects,
                    "request": request,
                },
            )
