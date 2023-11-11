from fastapi import HTTPException, APIRouter
from fastapi.responses import UJSONResponse
from database import get_session
from models import ItemList
from models import ResponseItem

from .functions import get_items_by_groups

router = APIRouter()


@router.post("/case/opening")
async def opening_case(items: ItemList):
    await get_items_by_groups(items=items.json())
    return {}
