from fastapi import APIRouter
from .functions import get_permission_id
from models import RequestPermissionID, ResponsePermission

router = APIRouter()

@router.get("/permission-id", response_model=ResponsePermission)
async def get_permission_id_(data: RequestPermissionID):
    permission = await get_permission_id(data.permission)
    return permission
