from fastapi import APIRouter, Depends
from .functions import get_role
from models import ResponseRole, RequestRoleID
from security import verify_admin

router = APIRouter()


@router.get("/role-id", response_model=ResponseRole)
async def get_role_id_(data: RequestRoleID, admin: str = Depends(verify_admin)):
    role = data.role
    response = await get_role(role)
    print(response)
    return response
