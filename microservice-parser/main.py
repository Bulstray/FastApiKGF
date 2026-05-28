from fastapi import FastAPI

import uvicorn

app = FastAPI(
    title="Fastapi parse tenders",
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8002,
    )
