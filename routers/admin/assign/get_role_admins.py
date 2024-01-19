from fastapi import APIRouter, Depends
from .functions import get_role_admins
from security import verify_admin

router = APIRouter()


@router.get("/role/emplyees")
async def get_role_admins_(role_name: str, admin: str = Depends(verify_admin)):
    admins = await get_role_admins(role_name)
    return admins
