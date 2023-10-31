from fastapi import APIRouter
from .functions import get_cases_items

router = APIRouter()


@router.get("/cases/items")
async def get_case_items_():
    case_data = await get_cases_items()
    return case_data
