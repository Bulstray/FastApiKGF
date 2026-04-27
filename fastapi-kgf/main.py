import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from admin import register_admin_views
from admin.auth import AdminAuth
from api import router
from app_lifespan import lifespan
from core.models import db_helper
from rest import router as main_router

app = FastAPI(lifespan=lifespan)

auth_backend = AdminAuth(secret_key="123132131")
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
        host="0.0.0.0",
        port=8000,
    )
