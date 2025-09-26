from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import pages,user,tasks
import uvicorn

app = FastAPI(title="ToDo App")
app.mount("/templates/css", StaticFiles(directory="templates/css"), name="static")
app.include_router(pages.router)
app.include_router(user.router)
app.include_router(tasks.router)
templates = Jinja2Templates(directory="/templates")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
