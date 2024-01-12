from fastapi import APIRouter, HTTPException, status
from .functions import get_case_item

router = APIRouter()


@router.get("/case/{case_id}/item/{item_id}")
async def get_case_item_(case_id: str, item_id: str):
    item = await get_case_item(case_id=case_id, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Предмет с ID '{item_id}' в кейсе с ID '{case_id}' не найден!",
        )
    return item
