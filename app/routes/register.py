from . import (root_router, templates)
from fastapi.responses import HTMLResponse
from fastapi import  Request

@root_router.get("/register", response_class=HTMLResponse)
async def register_view(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request,}
    )
