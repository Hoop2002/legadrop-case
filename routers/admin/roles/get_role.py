from fastapi import APIRouter, Depends
from .functions import get_role
from models import ResponseRole, RequestRoleName
from security import verify_admin

router = APIRouter()


# @router.get("/role-name", response_model=ResponseRole)
@router.get("/role-name")
async def get_role_(data: RequestRoleName, admin: str = Depends(verify_admin)):
    response = await get_role(data.role_id)
    return response
