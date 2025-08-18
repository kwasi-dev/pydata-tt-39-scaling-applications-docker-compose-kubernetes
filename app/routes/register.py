from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Request, Form, Depends
from app.models import User
from app.database import get_session

@root_router.get("/register", response_class=HTMLResponse)
async def register_view(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request,}
    )


@root_router.post("/register", response_class=RedirectResponse)
async def register_action(request: Request, session: AsyncSession = Depends(get_session),  name = Form(), email = Form(), password = Form(), password_confirm = Form()):

    pass