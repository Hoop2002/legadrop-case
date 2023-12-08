from fastapi import APIRouter
from security.token_functions import verify_admin
from .functions import get_emoployees_data

# from ..roles.functions.get_admin_role_module import get_role

router = APIRouter()

ROLE_MANAGEMENT_PERMISSION = "Просмотр сотрудников"


@router.get("/employees")
async def get_employees_():
    employees = await get_emoployees_data()
    return employees
