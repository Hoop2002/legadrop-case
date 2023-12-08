from fastapi import APIRouter, HTTPException, status
from .functions import get_permission_roles


router = APIRouter()


@router.get("/permission/roles")
async def get_permission_roles_(permission_name: str):
    try:
        roles = await get_permission_roles(permission_name)
        return {
            "permission_name": permission_name,
            "roles": [role.name for role in roles],
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
