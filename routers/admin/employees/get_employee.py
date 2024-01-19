from fastapi import APIRouter, Depends, HTTPException
from .functions import get_employee
from models import ResponseAdministrator
from security import verify_admin

router = APIRouter()


@router.get("/employee/{admin_id}", response_model=ResponseAdministrator)
async def get_employee_(admin_id: str, admin: str = Depends(verify_admin)):
    employee_data = await get_employee(admin_id)
    return employee_data
