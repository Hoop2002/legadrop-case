from fastapi import APIRouter, HTTPException, status 
from models import RequestCategoryDelete
from .functions import get_category, delete_category

router = APIRouter()


@router.delete("/category")
async def delete_category_(data: RequestCategoryDelete):
    category = await get_category(category_id = data.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    if await delete_category(category_id = data.category_id):
        return HTTPException(status_code=status.HTTP_200_OK, detail="Категория успешно удаленна")
    else: return HTTPException(status_code=status.HTTP_200_OK, detail="Категория не удаленна")