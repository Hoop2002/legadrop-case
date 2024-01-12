from fastapi import APIRouter, Depends
from models import RequestAdminID, ResponseAdministrator
from security.token_functions import verify_admin
from ..employees.functions import get_employee

router = APIRouter()


@router.get("/me", response_model=ResponseAdministrator)
async def admin_me(auth: RequestAdminID = Depends(verify_admin)):
    employee = await get_employee(admin_id=auth.admin_id)
    return employee
