from fastapi import FastAPI

from api import router

import uvicorn

app = FastAPI(
    title="Fastapi parse tenders",
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8002,
    )
