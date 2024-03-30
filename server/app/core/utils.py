import os
import string
import random
from io import BytesIO

from PIL import Image
from sqlalchemy.sql import select
from fastapi import UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from app.core.database import SessionLocal
from app.models.exercises import Exercise


class TempFileResponse(FileResponse):
    def __init__(self, path: str, filename: str, *args, **kwargs):
        super().__init__(path, *args, **kwargs)
        self.temp_file_path = path
        self.background = BackgroundTask(self.cleanup_temp_file)

    async def cleanup_temp_file(self):
        os.remove(self.temp_file_path)
        print(f"Temporary file {self.temp_file_path} has been deleted.")

    async def __call__(self, scope, receive, send):
        await super().__call__(scope, receive, send)
        await self.background()


def generate_random_password(length: int):
    charset = string.ascii_letters + string.digits
    return "".join(random.choices(charset, k=length))


async def compress_and_save_image(
        file: UploadFile,
        save_path: str,
        quality: int = 50,
        size: tuple = (400, 400)
):
    image = Image.open(BytesIO(await file.read()))
    image = image.resize(size)
    image.save(save_path, quality=quality, optimize=True)


async def insert_default_data():
    db = SessionLocal()

    # noinspection PyTypeChecker
    result = db.execute(select(Exercise).where(Exercise.id == "high_knees"))
    exists = result.scalars().first()

    if not exists:
        high_knees = Exercise(
            id="high_knees",
            name="High Knees",
            video_link="high_knees.mov",
            description="Бег на месте с высоким поднятием коленей - это как игра в ловкие ниндзя! Отличный способ "
                        "пробудить тело и дать заряд бодрости на весь день."
        )
        db.add(high_knees)

    # noinspection PyTypeChecker
    result = db.execute(select(Exercise).where(Exercise.id == "jumping_jacks"))
    exists = result.scalars().first()

    if not exists:
        jumping_jacks = Exercise(
            id="jumping_jacks",
            name="Jumping Jacks",
            video_link="jumping_jacks.mp4",
            description="Прыжки с разведением рук и ног, как звездочка, взлетающая в небо! Это не только весело, "
                        "но и отлично закачивает энергией на весь день."
        )
        db.add(jumping_jacks)
        
        
    # noinspection PyTypeChecker
    result = db.execute(select(Exercise).where(Exercise.id == "custom"))
    exists = result.scalars().first()

    if not exists:
        jumping_jacks = Exercise(
            id="custom",
            name="Пользовательская",
            video_link="",
            description="Индивидуальное упражнение, выполненное по вашей собственной воле. Повторы засчитываться не будут."
        )
        db.add(jumping_jacks)

    db.commit()
