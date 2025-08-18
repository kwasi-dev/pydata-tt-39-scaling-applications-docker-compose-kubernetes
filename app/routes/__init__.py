from pathlib import Path
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

MODULE_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = MODULE_ROOT.joinpath("templates")
STATIC_PATH = MODULE_ROOT.joinpath("static")

templates = Jinja2Templates(directory=TEMPLATE_PATH)
root_router = APIRouter()

from .login import *
from .register import *
from .dashboard import *