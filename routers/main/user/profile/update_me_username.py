from fastapi import APIRouter, Depends
from security.token_functions import verify_user
from .functions import update_me_username
from models import RequestUpdateMeUsername


router = APIRouter()


@router.put("/user/me/username")
async def update_me_username_(
    data: RequestUpdateMeUsername, user_id=Depends(verify_user)
):
    user_data = await update_me_username(user_id=user_id, username=data.username)
    return user_data
