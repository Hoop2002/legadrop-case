from fastapi import APIRouter
from .functions import get_users

router = APIRouter()


@router.get("/users")
async def get_users_():
    return await get_users()
