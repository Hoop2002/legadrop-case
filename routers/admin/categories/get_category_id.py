from fastapi import APIRouter, HTTPException, status, Depends
from models import RequestCategoryName, ResponceCategory
from .functions import get_category_by_name
from security import verify_admin

router = APIRouter()


@router.get("/category-id", response_model=ResponceCategory)
async def get_category_id_(
    data: RequestCategoryName, admin: str = Depends(verify_admin)
):
    category = await get_category_by_name(name=data.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория уже существует"
        )
    return category
