from fastapi import APIRouter
from .functions import get_role_admins

router = APIRouter()


@router.get("/role/emplyees")
async def get_role_admins_(role_name: str):
    admins = await get_role_admins(role_name)
    return admins