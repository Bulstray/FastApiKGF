import uvicorn
from fastapi import FastAPI

from app_lifespan import lifespan

app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app)
