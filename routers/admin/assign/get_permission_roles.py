from fastapi import APIRouter, HTTPException, status, Depends
from .functions import get_permission_roles
from security import verify_admin

router = APIRouter()


@router.get("/permission/roles")
async def get_permission_roles_(
    permission_name: str, admin: str = Depends(verify_admin)
):
    try:
        roles = await get_permission_roles(permission_name)
        return {
            "permission_name": permission_name,
            "roles": [role.name for role in roles],
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
