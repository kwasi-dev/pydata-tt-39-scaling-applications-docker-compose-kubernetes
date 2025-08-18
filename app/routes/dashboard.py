from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Depends, status
from app.utilities import get_flashed_messages, oauth2_scheme
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from app.models import User, TodoItem
from app.utilities import flash, verify_password, get_flashed_messages, get_current_user
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


@root_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_view(request: Request, user: Annotated[str, Depends(get_current_user)], session: AsyncSession = Depends(get_session),):
    user_todos = (await session.exec(
        select(TodoItem).where(TodoItem.user_id == user.id).order_by(desc(TodoItem.id))
    )).all()


    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "messages": get_flashed_messages(request), "user": user, "todo_items": user_todos}
    )
