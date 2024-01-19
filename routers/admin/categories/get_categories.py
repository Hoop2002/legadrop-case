from fastapi import APIRouter, Depends
from models import ResponseCategories
from .functions import get_categories

from security import verify_admin

router = APIRouter()


@router.get("/categories")
async def get_categories_(admin: str = Depends(verify_admin)):
    categories = await get_categories()
    return {"categories": categories}
