from fastapi import APIRouter, Depends
from security.token_functions import verify_admin
from .functions import get_emoployees_data
from security import verify_admin

# from ..roles.functions.get_admin_role_module import get_role
from security import verify_admin

router = APIRouter()

ROLE_MANAGEMENT_PERMISSION = "Просмотр сотрудников"


@router.get("/employees")
async def get_employees_(admin: str = Depends(verify_admin)):
    employees = await get_emoployees_data()
    return employees
