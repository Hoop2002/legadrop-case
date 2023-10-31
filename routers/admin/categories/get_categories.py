from fastapi import APIRouter
from models import ResponseCategories
from .functions import get_categories

router = APIRouter()

@router.get("/categories", response_model=ResponseCategories)
async def get_categories_():
    categories = await get_categories()
    return {"categories": categories}