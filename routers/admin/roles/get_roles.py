from fastapi import APIRouter
from .functions import get_roles
from models import ResponseRoles

router = APIRouter()


# response_model=ResponseRoles
@router.get("/roles")
async def get_roles_():
    roles = await get_roles()
    return roles
