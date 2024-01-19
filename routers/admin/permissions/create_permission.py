from fastapi import APIRouter, Depends
from .functions import create_permission
from models import RequestPermissionCreate, ResponsePermission
from security import verify_admin


router = APIRouter()


@router.post("/permission", response_model=ResponsePermission)
async def create_permission_(
    data: RequestPermissionCreate, admin: str = Depends(verify_admin)
):
    permission = data.permission
    response = await create_permission(permission)
    return response
