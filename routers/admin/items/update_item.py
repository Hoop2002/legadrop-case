from fastapi import APIRouter, HTTPException, status 
from models import RequestItemUpdate, ResponseItem
from .functions import get_item, update_item

router = APIRouter()


@router.put("/item", response_model=ResponseItem)
async def update_item_(data: RequestItemUpdate):
    item = await get_item(item_id=data.item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")

    item = await update_item(item_id=data.item_id, name=data.name, image=data.image)
    return item