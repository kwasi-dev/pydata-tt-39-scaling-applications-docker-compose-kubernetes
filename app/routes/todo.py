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
from app.schemas import TodoComplete

@root_router.post("/todo", response_class=RedirectResponse)
async def create_todo_action(request: Request, user: Annotated[str, Depends(get_current_user)], content=Form(), session: AsyncSession = Depends(get_session),):
    try:
        todo = TodoItem(
            content=content,
            user_id = user.id
        )
        session.add(todo)
        await session.commit()
        flash(request, f"Item successfully created", "success")
    except Exception as e:
        flash(request, f"An error has occurred {e}")
    
    return RedirectResponse(
            request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

@root_router.put("/todo/{item_id}", response_class=RedirectResponse)
async def update_todo_completeness_action(item_id: int, todo_complete:TodoComplete, request: Request, user: Annotated[str, Depends(get_current_user)], session: AsyncSession = Depends(get_session),):
    try:
        user_todo = (await session.exec(
            select(TodoItem).where(TodoItem.user_id == user.id, TodoItem.id == item_id)
        )).one_or_none()
           
        if not user_todo:
            flash(request, "Item not found")
        else:
            user_todo.is_complete = todo_complete.is_complete
            session.add(user_todo)
            await session.commit()
            flash(request, f"Item successfully updated", "success")
    except Exception as e:
        flash(request, f"An error has occurred {e}")
    finally:
        return RedirectResponse(
            request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    
    

