from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from security.token_functions import verify_user
from .functions import get_items_by_user
from routers.functions import get_user

from models.schemas import UserItemsListSchema, ItemRequestSchema


router = APIRouter()


@router.get("/user/items", response_model=UserItemsListSchema)
async def get_user_items(
    user_id=Depends(verify_user), page: int = 0, page_size: int = 20
):
    items = await get_items_by_user(
        user_id, filter_by={"active": True}, page_size=page_size, page=page
    )
    return items


@router.post("/user/sale_item")
async def sale_user_item(user_item_id: ItemRequestSchema, user_id=Depends(verify_user)):
    user = await get_user(user_id)
    item = await get_items_by_user(
        user_id, filter_by=dict(id=user_item_id.id, active=True)
    )
    item = item[0]
    if not item:
        return JSONResponse(
            content={"message": "Все предметы уже проданы"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    balance = user.balance + item.item.cost_in_rubles
    user_item = await item.update({"active": False})
    await user.update({"balance": balance})

    return user_item
