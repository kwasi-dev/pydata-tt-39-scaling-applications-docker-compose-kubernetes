from fastapi import FastAPI
from .routes import root_router, STATIC_PATH
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.include_router(root_router)
