from fastapi import APIRouter, HTTPException, status, Depends
from models import RequestCreateCategory, ResponceCategory
from .functions import create_category, get_category_by_name
from security import verify_admin

router = APIRouter()


@router.post("/category")
async def create_category_(
    data: RequestCreateCategory, admin: str = Depends(verify_admin)
):
    category = await get_category_by_name(data.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Категория уже существует"
        )

    category = await create_category(data.name)
    return category
