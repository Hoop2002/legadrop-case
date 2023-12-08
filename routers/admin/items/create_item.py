from fastapi import APIRouter, HTTPException, status, UploadFile, Form, File
from models import RequestCreateItem, RequestItem, ResponseItem
from .functions import create_item, get_item_by_name, get_item
from models import Item
from pathlib import Path

IMAGES_PATH = "images/items"

router = APIRouter()


@router.post("/item", response_model=ResponseItem)
async def create_item_(
    name: str = Form(...),
    cost: int = Form(...),
    gem_cost: int = Form(...),
    color: str = Form(...),
    image: UploadFile = File(...),
):
    item = await get_item_by_name(name)
    if item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Предмет уже существует"
        )
    image_path = Path(IMAGES_PATH) / f"{name}.jpg"
    with image_path.open("wb") as buffer:
        content = await image.read()
        buffer.write(content)

    data = Item(
        name=name, cost=cost, gem_cost=gem_cost, color=color, image=str(image_path)
    )
    item = await create_item(data)
    return item
