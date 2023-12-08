from fastapi import APIRouter
from .functions import get_permissions
from models import ResponsePermissions


router = APIRouter()


# @router.get("/permissions", response_model=ResponsePermissions)
@router.get("/permissions")
async def get_permissions_():
    permissions = await get_permissions()
    return permissions
