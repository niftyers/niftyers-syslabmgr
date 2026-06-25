from core.settings import settings
from fastapi import FastAPI
import uvicorn

from api.auth import router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to Lab Central"}

app.include_router(
    router,
    prefix="/api/auth",
    tags=["Authentication"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG
    )