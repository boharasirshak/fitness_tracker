import string
import random
from io import BytesIO

from PIL import Image
from fastapi import UploadFile


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
