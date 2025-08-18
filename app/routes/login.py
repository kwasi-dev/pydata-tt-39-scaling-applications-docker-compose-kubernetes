from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form, Depends, status
from app.utilities import get_flashed_messages
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import User
from app.utilities import flash, verify_password, get_flashed_messages, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Union

@root_router.get("/", response_class=RedirectResponse)
async def root_redirect_login(request: Request):
    return RedirectResponse(
            request.url_for("login_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )


@root_router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "messages": get_flashed_messages(request)}
    )

@root_router.post("/login", response_class=RedirectResponse)
async def login_action(request: Request,  form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session),):
    user = (await session.exec(
        select(User).where(User.email == form_data.username)
    )).one_or_none()


    if not user or not verify_password(form_data.password, user.password):
        flash(request, "Incorect credentials! Please try again", "error")
        return RedirectResponse(
            request.url_for("login_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    
    # Generate tokens and set session
    response =  RedirectResponse(
            request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    token = create_access_token({"sub": user.email})
    response.set_cookie("access_token", token, httponly=True, secure=True, samesite="strict",path="/")

    return response

