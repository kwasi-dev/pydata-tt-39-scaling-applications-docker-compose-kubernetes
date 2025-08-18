from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Depends, status
from app.utilities import get_flashed_messages
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import User
from app.utilities import flash, verify_password, get_flashed_messages


@root_router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "messages": get_flashed_messages(request)}
    )

@root_router.post("/login", response_class=RedirectResponse)
async def login_action(request: Request, session: AsyncSession = Depends(get_session),  email = Form(), password = Form()):
    user = (await session.exec(
        select(User).where(User.email == email)
    )).one_or_none()

    if not user or not verify_password(password, user.password):
        flash(request, "Incorect credentials! Please try again", "error")
        return RedirectResponse(
            request.url_for("login_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    
    # Generate tokens and set session
    return RedirectResponse(
            request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )


