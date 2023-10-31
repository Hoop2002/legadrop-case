import os
import random
import string

from fastapi import UploadFile
from pathlib import Path


def id_genrator():
    first = random.choice(string.ascii_uppercase)
    second = random.choice(string.ascii_lowercase)
    third = random.choice(string.digits)
    alphabet = string.ascii_letters + string.digits
    remaining = ''.join(random.choice(alphabet) for _ in range(6))
    return first + second + third + remaining


async def save_image(image_name: str, upload_image: UploadFile, path: str) -> Path:
    image_path = Path(path) / f"{image_name}.jpg"
    with image_path.open("wb") as buffer:
        content = await upload_image.read()
        buffer.write(content)
    return image_path


async def update_image(image_name: str, upload_image: UploadFile, path: str) -> Path:
    image_path = Path(path) / f"{image_name}.jpg"
    if image_path.exists():
        os.remove(image_path)
    with image_path.open("wb") as buffer:
        content = await upload_image.read()
        buffer.write(content)
    return image_path


def delete_image(image_name: str, path: str) -> bool:
    image_path = Path(path) / f"{image_name}.jpg"
    if image_path.exists():
        os.remove(image_path)
        return True
    return False
