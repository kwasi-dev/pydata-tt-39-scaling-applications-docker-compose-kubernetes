from fastapi import FastAPI
from .routes import root_router, STATIC_PATH
from fastapi.staticfiles import StaticFiles
from .database import init_db
from starlette.middleware.sessions import SessionMiddleware
from .settings import get_settings

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.add_middleware(SessionMiddleware, secret_key=get_settings().secret_key)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router(root_router)
