from fastapi import HTTPException, APIRouter, Depends
from models import ItemList
from models import ResponseItem

from .functions import get_items_by_groups, get_item

from security import verify_user

router = APIRouter()


@router.post("/case/opening")
async def opening_case(items: ItemList, user_id: str = Depends(verify_user)):
    
    items_group, group_ext = await get_items_by_groups(items=items.model_dump())
    item = await get_item(
        items=items_group, uid=user_id, group_id=group_ext
    )
    return item[-1]
