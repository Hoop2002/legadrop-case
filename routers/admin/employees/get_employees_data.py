from fastapi import APIRouter, Depends
from .functions import get_emoployees_data
from security import verify_admin

router = APIRouter()


@router.get("/employees")
async def get_employees_(admin: str = Depends(verify_admin)):
    employees = await get_emoployees_data()
    return employees
