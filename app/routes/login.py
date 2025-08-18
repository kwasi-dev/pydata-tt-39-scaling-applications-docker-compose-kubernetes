from . import (root_router, templates)
from fastapi.responses import HTMLResponse
from fastapi import  Request
from app.utilities import get_flashed_messages

@root_router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "messages": get_flashed_messages(request)}
    )
