from . import (root_router, templates)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Request, Depends, Form, status, Query

@root_router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request,}
    )
