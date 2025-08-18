from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Request, Form, Depends, status
from app.models import User
from app.database import get_session
from app.utilities import flash, hash_password, get_flashed_messages

@root_router.get("/register", response_class=HTMLResponse)
async def register_view(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request, "messages": get_flashed_messages(request)}
    )


@root_router.post("/register", response_class=RedirectResponse)
async def register_action(request: Request, session: AsyncSession = Depends(get_session),  name = Form(), email = Form(), password = Form(), password_confirm = Form()):
    user = (await session.exec(
        select(User).where(User.email == email)
    )).one_or_none()

    if user:
        flash(request, "The email you have entered already exists, try logging in instead!", "error")
        return RedirectResponse(
            request.url_for("login_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        ) 
    if password != password_confirm:
        flash(request, "The passwords do not match! Try again", "error")
        return RedirectResponse(
            request.url_for("register_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        ) 
    
    user = User(
        full_name=name,
        email=email,
        password=hash_password(password)
    )
    session.add(user)
    await session.commit()

    flash(request, "Account registered successfully", "success")

    return RedirectResponse(
            request.url_for("login_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        ) 
