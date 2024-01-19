from fastapi import APIRouter, Depends
from .functions import get_permission_id
from models import RequestPermissionID, ResponsePermission
from security import verify_admin

router = APIRouter()


@router.get("/permission-id", response_model=ResponsePermission)
async def get_permission_id_(
    data: RequestPermissionID, admin: str = Depends(verify_admin)
):
    permission = await get_permission_id(data.permission)
    return permission
