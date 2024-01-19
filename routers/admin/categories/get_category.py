from fastapi import APIRouter, HTTPException, status, Depends
from models import RequestCategory, ResponceCategory
from .functions import get_category
from security import verify_admin

router = APIRouter()


@router.get("/category", response_model=ResponceCategory)
async def get_category_(data: RequestCategory, admin: str = Depends(verify_admin)):
    category = await get_category(category_id=data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )
    return category
