from fastapi import APIRouter

from .functions import get_admin_permissions

router = APIRouter()


@router.get("/employee/permissions")
async def get_admin_permissions_(user_name: str):
    permissions = await get_admin_permissions(user_name)
    return permissions
