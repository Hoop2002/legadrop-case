from fastapi import APIRouter, Depends
from .functions import get_permissions
from models import ResponsePermissions
from security import verify_admin

router = APIRouter()


# @router.get("/permissions", response_model=ResponsePermissions)
@router.get("/permissions")
async def get_permissions_(admin: str = Depends(verify_admin)):
    permissions = await get_permissions()
    return permissions
