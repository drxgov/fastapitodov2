from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.templating import Jinja2Templates
import utils
import os

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/")
async def get_main():
    # Если main.html в папке templates
    return templates.TemplateResponse("main.html", {"request": {}})

@router.get("/main")
async def main_page(request: Request, db: Session = Depends(utils.get_db)):
    current_user = utils.get_current_user_from_request(request, db)
    return templates.TemplateResponse("list.html", {"request": request, "user": current_user})