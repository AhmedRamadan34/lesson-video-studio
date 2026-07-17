from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid
from pathlib import Path
from app.services.video_service import VideoService
from app.config import IMAGE_DIR, AUDIO_DIR, OUTPUT_VIDEO

import shutil

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if username == "admin" and password == "123456":

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request
            }
        )

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": "Invalid username or password."
        }
    )


@router.post("/upload")
async def upload_files(
    images: list[UploadFile] = File(...),
    audios: list[UploadFile] = File(...)
):

    # حذف الملفات القديمة
    for folder in (IMAGE_DIR, AUDIO_DIR):
        for file in folder.iterdir():
            if file.is_file():
                file.unlink()

    # حفظ الصور
    for image in images:
        with open(IMAGE_DIR / image.filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # حفظ ملفات الصوت
    for audio in audios:
        with open(AUDIO_DIR / audio.filename, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

    # إنشاء الفيديو
    video_name = f"{uuid.uuid4().hex}.mp4"

    output_video = OUTPUT_VIDEO.parent / video_name

    VideoService.generate_video(
        IMAGE_DIR,
        AUDIO_DIR,
        output_video
    )

    return {
        "message": "Video generated successfully",
        "video": f"/output/{video_name}"
    }