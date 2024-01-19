from fastapi import APIRouter, Depends
from .functions import get_cases_items
from security import verify_admin

router = APIRouter()


@router.get("/cases/items")
async def get_case_items_(admin: str = Depends(verify_admin)):
    case_data = await get_cases_items()
    return case_data
