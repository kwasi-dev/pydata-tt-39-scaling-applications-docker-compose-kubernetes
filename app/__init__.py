from fastapi import FastAPI
from .routes import root_router, STATIC_PATH
from fastapi.staticfiles import StaticFiles
from .database import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router(root_router)
