from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Request, Form, Depends, status
from app.models import TokenBlacklist
from app.database import get_session
from app.utilities import flash, hash_password, get_flashed_messages
from typing import Annotated
from app.utilities import flash, verify_password, get_flashed_messages, get_current_user



@root_router.get("/logout", response_class=RedirectResponse)
async def logout_action(request: Request, user: Annotated[str, Depends(get_current_user)], session: AsyncSession = Depends(get_session), ):
    token = request.cookies.get("access_token")

    blacklisted_token = TokenBlacklist(
        token=token
    )
    session.add(blacklisted_token)
    await session.commit()

    response =  RedirectResponse(
            request.url_for("login_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        ) 
    response.delete_cookie(key="access_token")
    
    return response