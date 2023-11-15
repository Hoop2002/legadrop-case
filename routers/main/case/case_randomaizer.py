from fastapi import HTTPException, APIRouter
from models import ItemList
from models import ResponseItem

from .functions import get_items_by_groups, get_item

router = APIRouter()


@router.post("/case/opening")
async def opening_case(items: ItemList):
    items_group, group_ext = await get_items_by_groups(items=items.model_dump())
    item = await get_item(items=items_group, uid=items.model_dump()['user']['uid'], group_id=group_ext)
    return item[-1]