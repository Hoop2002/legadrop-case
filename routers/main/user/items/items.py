from fastapi import APIRouter, Depends
from security.token_functions import verify_user
from .functions import get_items_by_user

from models.schemas import UserItemsList


router = APIRouter()


@router.get("/user/items", response_model=UserItemsList)
async def get_user_items(user_id=Depends(verify_user), offset: int = 0, limit: int = 20):
    items = await get_items_by_user(user_id)
    return items[offset: offset + limit]
