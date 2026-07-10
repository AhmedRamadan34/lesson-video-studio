from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
IMAGE_DIR = UPLOAD_DIR / "images"
AUDIO_DIR = UPLOAD_DIR / "audio"

OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

for folder in [
    IMAGE_DIR,
    AUDIO_DIR,
    OUTPUT_DIR,
    TEMP_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

OUTPUT_VIDEO = OUTPUT_DIR / "lesson_video.mp4"