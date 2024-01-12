from fastapi import APIRouter
from .functions import get_role
from models import ResponseRole, RequestRoleName

router = APIRouter()


# @router.get("/role-name", response_model=ResponseRole)
@router.get("/role-name")
async def get_role_(data: RequestRoleName):
    response = await get_role(data.role_id)
    return response
