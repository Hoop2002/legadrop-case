from fastapi import APIRouter, Depends
from .functions import get_roles
from models import ResponseRoles
from security import verify_admin

router = APIRouter()


# response_model=ResponseRoles
@router.get("/roles")
async def get_roles_(admin: str = Depends(verify_admin)):
    roles = await get_roles()
    return roles
