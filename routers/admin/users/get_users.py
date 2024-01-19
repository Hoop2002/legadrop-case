from fastapi import APIRouter, Depends
from .functions import get_users
from security import verify_admin

router = APIRouter()


@router.get("/users")
async def get_users_(admin: str = Depends(verify_admin)):
    return await get_users()
