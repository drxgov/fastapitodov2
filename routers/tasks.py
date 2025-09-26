from fastapi import APIRouter, Depends, Request,Form
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import models
import utils
import os

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/main")
async def main_page(request: Request, db: Session = Depends(utils.get_db)):
    current_user = utils.get_current_user_from_request(request, db)
    if isinstance(current_user, RedirectResponse):
        return current_user

    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    print("Tasks for user", current_user.id, "->", tasks)

    return templates.TemplateResponse("list.html", {
        "request": request,
        "user": current_user,
        "tasks": tasks
    })

@router.post("/tasks")
async def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(utils.get_db)
):
    current_user = utils.get_current_user_from_request(request, db)
    if isinstance(current_user, RedirectResponse):
        return current_user

    # Создаём новую задачу
    new_task = models.Task(
        title=title,
        description=description,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    print("Task created:", new_task.id, new_task.title, new_task.user_id, current_user.id)
    # Перенаправляем обратно на /main
    return RedirectResponse(url="/main", status_code=303)



@router.post('/tasks/{task_id}/complete')
async def complete_task(task_id: int, request: Request, db: Session = Depends(utils.get_db)):
    current_user = utils.get_current_user_from_request(request, db)
    if isinstance(current_user, RedirectResponse):
        return current_user
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if task:
        task.is_completed = True
        db.commit()

    return RedirectResponse(url="/main", status_code=303)

@router.post('/tasks/{task_id}/delete')
async def delete_task(task_id: int, request: Request, db: Session = Depends(utils.get_db)):
    current_user = utils.get_current_user_from_request(request, db)
    if isinstance(current_user, RedirectResponse):
        return current_user
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if task:
        db.delete(task)
        db.commit()

    return RedirectResponse(url="/main", status_code=303)