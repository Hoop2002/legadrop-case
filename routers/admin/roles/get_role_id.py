from fastapi import APIRouter
from .functions import get_role
from models import ResponseRole, RequestRoleID


router = APIRouter()


@router.get("/role-id", response_model=ResponseRole)
async def get_role_id_(data: RequestRoleID):
    role = data.role
    response = await get_role(role)
    print(response)
    return response
