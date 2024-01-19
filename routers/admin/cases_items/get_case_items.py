from fastapi import APIRouter, HTTPException, status, Depends
from .functions import get_case_items
from security import verify_admin

router = APIRouter()


@router.get("/case/{case_id}/items")
async def get_case_items_(case_id: str, admin: str = Depends(verify_admin)):
    items = await get_case_items(case_id=case_id)
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Кейс с ID '{case_id}' не найден!",
        )
    return items
