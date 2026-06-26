from api.auth import router
from core.settings import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.mount(
    "/assets",
    StaticFiles(directory="web/assets"),
    name="assets"
)

@app.get("/")
async def root():
    return FileResponse("web/index.html")


@app.get("/{path:path}")
async def spa(path: str):
    if path.startswith("api"):
        return {"detail": "Not Found"}

    return FileResponse("web/index.html")