from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from core.config.settings import SESSION_COOKIE_NAME
from core.schemas import UserRead, UserUpdateForm
from dependencies.session_auth import get_current_user
from dependencies.user import UserServiceFactory
from storage.redis.session import save_session
from templating.jinja_template import templates
from storage.db.crud_project import get_all_projects

from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper

from storage.db.crud_user import update_data_user

router = APIRouter(prefix="/profile")


@router.get("/", name="profile:page")
async def profile_page(
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
        "profile.html",
        context={
            "user": current_user,
            "request": request,
            "projects": await get_all_projects(session),
        },
    )


@router.post("/", name="profile:update")
async def update_profile(
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
    projects = await get_all_projects(session)
    async with request.form() as form_data:

        try:
            user_update = UserUpdateForm.model_validate(form_data)

        except TypeError:
            return templates.TemplateResponse(
                "profile.html",
                context={
                    "user": current_user,
                    "projects": projects,
                    "request": request,
                    "error": "Ошибка валидации. "
                    "Проверьте правильность введённых данных.",
                },
            )

        else:
            await update_data_user(
                user_update,
                current_user.id,
            )

            session_id = cast(
                "str",
                request.cookies.get(SESSION_COOKIE_NAME),
            )

            if user_update.email:
                current_user.email = user_update.email
                await save_session(session_id, current_user)

            return templates.TemplateResponse(
                "profile.html",
                context={
                    "user": current_user,
                    "projects": projects,
                    "request": request,
                    "success": "Данные успешно сохранены",
                },
            )
