from fastapi import APIRouter, HTTPException, status
from .functions import get_role_permissions


router = APIRouter()


@router.get("/role/permissions/")
async def get_role_permissions_(role_name: str):
    try:
        permissions = await get_role_permissions(role_name)
        return {
            "role_name": role_name,
            "permissions": [permission.name for permission in permissions],
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
