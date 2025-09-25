from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory="/templates")

@router.get("/")
async def get_main():
    return FileResponse(BASE_DIR / "main.html")

@router.get("/login")
async def get_login():
    return FileResponse(BASE_DIR / "login.html")
