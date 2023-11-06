from fastapi import APIRouter, HTTPException, status 
from models import RequestItem, ResponseItem
from .functions import get_item


router = APIRouter()


@router.get("/items/{item_id}", response_model=ResponseItem)
async def get_item_(item_id: str):
    item = await get_item(item_id = item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    return item
