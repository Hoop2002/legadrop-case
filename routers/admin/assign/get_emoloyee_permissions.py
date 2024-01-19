from fastapi import APIRouter, Depends

from .functions import get_admin_permissions
from security import verify_admin

router = APIRouter()


@router.get("/employee/permissions")
async def get_admin_permissions_(user_name: str, admin: str = Depends(verify_admin)):
    permissions = await get_admin_permissions(user_name)
    return permissions
