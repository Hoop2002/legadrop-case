from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from security.token_functions import verify_user
from .functions import get_items, get_item_by_id
from routers.functions import get_user

from models.schemas import ItemsListSchema, ItemRequestSchema
from models import UserItems


router = APIRouter()


@router.get("/shop/items", response_model=ItemsListSchema)
async def get_user_items(page: int = 0, page_size: int = 20):
    items = await get_items({"sale": True}, page_size=page_size, page=page)
    return items


@router.post("/shop/buy_item")
async def buy_item(item: ItemRequestSchema, user_id=Depends(verify_user)):
    user = await get_user(user_id)
    _item = await get_item_by_id(item.id)
    if not _item:
        return JSONResponse(
            content={"message": "Все предметы уже проданы"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if user.balance >= _item.cost_in_rubles:
        balance = user.balance - _item.cost_in_rubles
        user_item = await UserItems.create(user=user, item=_item)
        await user.update({"balance": balance})

        return user_item
    else:
        return JSONResponse(content={'message': 'Не хватает средств'}, status_code=status.HTTP_400_BAD_REQUEST)
