from fastapi import APIRouter, Depends
from security.token_functions import verify_user
from .functions import get_me


router = APIRouter()


@router.get("/user/me")
async def user_me(user_id=Depends(verify_user)):
    user_data = await get_me(user_id=user_id)
    return user_data
