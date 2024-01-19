from fastapi import APIRouter, Depends
from .functions import get_permission
from models import RequestPermission, ResponsePermission
from security import verify_admin

router = APIRouter()


@router.get("/permission", response_model=ResponsePermission)
async def get_permission_(data: RequestPermission, admin: str = Depends(verify_admin)):
    permission = await get_permission(data.permission_id)
    return permission
