import uvicorn
from fastapi import FastAPI

from api import router
from app_lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app")
