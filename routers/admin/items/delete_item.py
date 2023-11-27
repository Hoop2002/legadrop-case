from fastapi import APIRouter, HTTPException, status 
from models import RequestItemDelete
from .functions import get_item, delete_item


router = APIRouter()


@router.delete("/item")
async def delete_item_(data: RequestItemDelete):
    item = await get_item(item_id=data.item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")

    item = await delete_item(item_id=data.item_id)
    return {"data": item, "detail": "Предмет успешно удален"}
