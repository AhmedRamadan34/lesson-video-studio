from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router

app = FastAPI(
    title="Lesson Video Studio",
    version="1.0.0"
)

app.mount(
    "/output",
    StaticFiles(directory="app/output"),
    name="output"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(router)