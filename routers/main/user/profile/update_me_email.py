from fastapi import APIRouter, Depends
from security.token_functions import verify_user
from .functions import update_me_email
from models import RequestUpdateMeEmail


router = APIRouter()


@router.put("/user/me/email")
async def update_me_email_(data: RequestUpdateMeEmail, user_id=Depends(verify_user)):
    user_data = await update_me_email(user_id=user_id, email=data.email)
    return user_data
