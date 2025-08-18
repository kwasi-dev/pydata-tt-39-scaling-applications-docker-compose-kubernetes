from fastapi import FastAPI
from .routes import root_router

app = FastAPI()
app.include_router(root_router)