import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from admin import register_admin_views
from admin.auth import AdminAuth
from api import router
from app_lifespan import lifespan
from core.config import settings, BASE_DIR
from core.models import db_helper
from rest import router as main_router

STATIC_PATH = BASE_DIR / "static"

app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_PATH),
    name="static",
)

auth_backend = AdminAuth(
    secret_key=settings.secret_key_admin.secret_key,
)
admin = Admin(
    app,
    session_maker=db_helper.session_factory,
    authentication_backend=auth_backend,
)

register_admin_views(admin)
app.include_router(router)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        # host="0.0.0.0",
        # port=8000,
    )
