import stat
from fastapi import APIRouter, HTTPException, status, Request
from models import RequestItemUpdate, ResponseItem
from .functions import get_item, update_item

router = APIRouter()


@router.put("/item")
async def update_item_(request: Request, data: dict):
    
    if not data.get("item_id", False):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="key 'item_id' not found", headers=request.headers)
    
    item = await get_item(item_id=data.get("item_id"))


    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")

    item = await update_item(data=data)
    return item