from fastapi import APIRouter, HTTPException, status, Depends
from .functions import get_role_permissions
from security import verify_admin

router = APIRouter()


@router.get("/role/permissions/")
async def get_role_permissions_(role_name: str, admin: str = Depends(verify_admin)):
    try:
        permissions = await get_role_permissions(role_name)
        return {
            "role_name": role_name,
            "permissions": [permission.name for permission in permissions],
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
