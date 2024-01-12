from fastapi import APIRouter, HTTPException, status
from models import RequestCategoryUpdate, ResponceCategory
from .functions import update_category, get_category

router = APIRouter()


@router.put("/category", response_model=ResponceCategory)
async def update_category_(data: RequestCategoryUpdate):
    category = await get_category(category_id=data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    category = await update_category(category_id=data.category_id, name=data.name)
    return category
