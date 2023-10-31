from fastapi import APIRouter, Depends
from security.token_functions import verify_user
from .functions import update_me_locale
from models import RequestUpdateMeLocale


router = APIRouter()


@router.put("/user/me/locale")
async def update_me_locale_(data: RequestUpdateMeLocale, user_id=Depends(verify_user)):
    user_data = await update_me_locale(user_id=user_id, locale=data.locale)
    return user_data
