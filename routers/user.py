from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
import database
import utils
import models


router = APIRouter(tags=["users"])
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally: 
        db.close()

@router.get("/register")
async def registerPage(request: Request):
    return templates.TemplateResponse("register.html",{'request': request})

@router.post("/register")
async def registerUser(request: Request, username:str = Form(...), password:str = Form(...),confirmPassword:str = Form(...),db:Session = Depends(get_db)):
    if password != confirmPassword:
        return templates.TemplateResponse("register.html",{
            'request': request,
            'message': 'введеные пароли не совпадают',
            'succes': False,
            })
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        return templates.TemplateResponse("register.html",{
            'request': request,
            'message': 'такой пользователь уже существует',
            'succes': False,
            })
    hashedPW = utils.hashPass(password)
    newUser = models.User(username = username,hashedPassword = hashedPW)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return templates.TemplateResponse("register.html", {
        "request": request,
        "message": f"Пользователь {username} успешно зарегистрирован",
        "success": True
    })

@router.get("/login")
async def loginPage(request: Request):
    return templates.TemplateResponse("login.html",{'request': request})


@router.post("/login")
async def loginUser(request: Request,username: str = Form(...), password: str = Form(...),db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return templates.TemplateResponse("register.html",{
            'request': request,
            'message': 'такого пользователя не существует',
            'succes': False,
            })
    if not utils.verify_password(password, db_user.hashedPassword):
        return templates.TemplateResponse("register.html", {
            'request': request,
            'message': 'неправильно введен пароль',
            'success': False,
        })
    access_token = utils.create_access_token(data={"sub": db_user.username})
    response = RedirectResponse(url='/main', status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # если HTTPS, ставь True
        samesite="lax",
        path="/"
    )
    return response