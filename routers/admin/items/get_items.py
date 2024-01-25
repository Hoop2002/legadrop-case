from fastapi import APIRouter, Depends
from models import ResponseItems
from .functions import get_items
from security import verify_admin

router = APIRouter()


@router.get("/items")
async def get_items_(
    admin: str = Depends(verify_admin), offset: int = 0, limit: int = 20
):
    items = await get_items()

    return items
