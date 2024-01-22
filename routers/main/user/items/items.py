from fastapi import APIRouter, Depends
from security.token_functions import verify_user
from .functions import get_items_by_user

from models.schemas import UserItemsListSchema


router = APIRouter()


@router.get("/user/items", response_model=UserItemsListSchema)
async def get_user_items(
    user_id=Depends(verify_user), page: int = 0, page_size: int = 20
):
    items = await get_items_by_user(user_id, page_size=page_size, page=page)
    return items
