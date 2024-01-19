from fastapi import APIRouter, HTTPException, status, Depends
from models import RequestItem, ResponseItem
from .functions import get_item
from security import verify_admin

router = APIRouter()


@router.get("/items/{item_id}")
async def get_item_(item_id: str, admin: str = Depends(verify_admin)):
    item = await get_item(item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден"
        )
    return item
