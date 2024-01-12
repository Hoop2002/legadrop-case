from fastapi import APIRouter
from models import ResponseItems
from .functions import get_items

router = APIRouter()


@router.get("/items")
async def get_items_():
    items = await get_items()

    return items
