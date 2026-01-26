import uvicorn
from fastapi import FastAPI

from api import router
from app_lifespan import lifespan
from rest import router as main_router

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
