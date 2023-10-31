from fastapi import APIRouter
from .functions import get_emoployees_data

router = APIRouter()


@router.get("/employees")
async def get_employees_():
    employees = await get_emoployees_data()
    return employees