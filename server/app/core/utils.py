import string
import random
from io import BytesIO

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.sql import select

from app.core.database import SessionLocal
from app.models.users import User
from app.models.exercises import Exercise
from app.models.workouts import Workout


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
    result = await db.execute(select(Exercise).where(Exercise.id == "high_knees"))
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
    result = await db.execute(select(Exercise).where(Exercise.id == "jumping_jacks"))
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

    await db.commit()
