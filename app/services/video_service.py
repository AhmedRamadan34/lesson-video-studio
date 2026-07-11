from pathlib import Path
from mutagen import File as MutagenFile
from moviepy import (
    ImageClip,
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    concatenate_videoclips,
)

from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
)


class VideoService:

    @staticmethod
    def validate_files(images: list[Path], audios: list[Path]):

        if len(images) == 0:
            raise ValueError("No images found.")

        if len(audios) == 0:
            raise ValueError("No audio files found.")

        if len(images) != len(audios):
            raise ValueError(
                f"Images ({len(images)}) != Audios ({len(audios)})"
            )

    @staticmethod
    def get_audio_duration(audio_path: Path) -> float:

        audio = MutagenFile(audio_path)

        if audio is None:
            raise ValueError(
                f"Unsupported audio format: {audio_path.name}"
            )

        if not hasattr(audio, "info") or audio.info is None:
            raise ValueError(
                f"Cannot read audio information: {audio_path.name}"
            )

        return round(audio.info.length, 2)

    SUPPORTED_IMAGES = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp"
    }

    SUPPORTED_AUDIO = {
        ".mp3",
        ".wav",
        ".m4a",
        ".aac",
        ".ogg",
        ".flac",
        ".wma"
    }

    @staticmethod
    def build_scene_list(image_dir: Path, audio_dir: Path):

        images = {}
        audios = {}

        # جمع الصور
        for image in image_dir.iterdir():
            if image.suffix.lower() in VideoService.SUPPORTED_IMAGES:
                images[image.stem.lower()] = image

        # جمع ملفات الصوت
        for audio in audio_dir.iterdir():
            if audio.suffix.lower() in VideoService.SUPPORTED_AUDIO:
                audios[audio.stem.lower()] = audio

        missing_audio = []
        missing_image = []
        scenes = []

        # مطابقة الصورة مع الصوت بنفس الاسم
        for name, image in images.items():

            if name not in audios:
                missing_audio.append(image.name)
                continue

            audio = audios[name]

            scenes.append({
                "image": image,
                "audio": audio,
                "duration": VideoService.get_audio_duration(audio)
            })

        # البحث عن ملفات صوت بدون صورة
        for name, audio in audios.items():
            if name not in images:
                missing_image.append(audio.name)

        if missing_audio:
            raise ValueError(
                f"No matching audio for: {', '.join(missing_audio)}"
            )

        if missing_image:
            raise ValueError(
                f"No matching image for: {', '.join(missing_image)}"
            )

        return sorted(
            scenes,
            key=lambda x: x["image"].stem.lower()
        )

    @staticmethod
    def generate_video(
        image_dir: Path,
        audio_dir: Path,
        output_path: Path
    ):

        scenes = VideoService.build_scene_list(
            image_dir,
            audio_dir
        )

        clips = []

        VIDEO_SIZE = (1280, 720)

        for scene in scenes:

            audio_clip = AudioFileClip(str(scene["audio"]))

            image = (
                ImageClip(str(scene["image"]))
                .resized(height=720)
                .with_duration(audio_clip.duration)
            )

            background = (
                ColorClip(
                    size=VIDEO_SIZE,
                    color=(0, 0, 0)
                )
                .with_duration(audio_clip.duration)
            )

            final_clip = CompositeVideoClip(
                [
                    background,
                    image.with_position("center")
                ],
                size=VIDEO_SIZE
            ).with_audio(audio_clip)

            clips.append(final_clip)

        final_video = concatenate_videoclips(
            clips,
            method="compose"
        )

        final_video.write_videofile(
            str(output_path),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=2
        )

        final_video.close()

        for clip in clips:
            clip.close()