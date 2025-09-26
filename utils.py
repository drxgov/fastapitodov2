from passlib.context import CryptContext
from fastapi import HTTPException, status, Cookie, Depends, Request
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from sqlalchemy.orm import Session 
import database
import models

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "okak"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPass(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_from_request(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url='/login', status_code=303)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return RedirectResponse(url='/login', status_code=303)
    except jwt.JWTError:
        return RedirectResponse(url='/login', status_code=303)

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        return RedirectResponse(url='/login', status_code=303)

    return user