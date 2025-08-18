from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Depends, status
from app.utilities import get_flashed_messages
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import User, TodoItem
from app.utilities import flash, verify_password, get_flashed_messages, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Union
from app.utilities import flash, verify_password, get_flashed_messages, get_current_user


@root_router.post("/todo", response_class=RedirectResponse)
async def create_todo_action(request: Request, user: Annotated[str, Depends(get_current_user)], content=Form(), session: AsyncSession = Depends(get_session),):
    try:
        todo = TodoItem(
            content=content,
            user_id = user.id
        )
        session.add(user)
        await session.commit()
    except Exception as e:
        flash(request, f"An error has occurred {e}")
    
    return RedirectResponse(
            request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
