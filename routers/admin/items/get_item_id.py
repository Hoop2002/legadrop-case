from fastapi import APIRouter, HTTPException, status, Depends
from models import RequestItemName, ResponseItem
from .functions import get_item_by_name
from security import verify_admin

router = APIRouter()


@router.get("/item-id", response_model=ResponseItem)
async def get_item_id_(data: RequestItemName, admin: str = Depends(verify_admin)):
    item = await get_item_by_name(name=data.name)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден"
        )
    return item
