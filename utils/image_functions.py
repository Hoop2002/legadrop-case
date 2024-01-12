import os
from fastapi import UploadFile
from pathlib import Path


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


async def update_user_image(image_name: str, upload_image: UploadFile) -> Path:
    image_path = Path("images/users") / f"{image_name}.jpg"
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
