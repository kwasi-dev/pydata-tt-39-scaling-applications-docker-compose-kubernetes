from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Depends, status
from app.utilities import get_flashed_messages
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import User
from app.utilities import flash, verify_password, get_flashed_messages

@root_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_view(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "messages": get_flashed_messages(request)}
    )
