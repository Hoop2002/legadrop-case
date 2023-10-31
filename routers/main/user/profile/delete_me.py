from fastapi import APIRouter, HTTPException, status, Depends
from security.token_functions import verify_user
from security.password_functions import verify_password
from .functions import get_me, delete_me
from models import RequestDeleteMe


router = APIRouter()


@router.delete("/user/me/username")
async def update_me_username_(
    data: RequestDeleteMe, user_id=Depends(verify_user)
):
    user_data = await get_me(user_id)
    if not user_data:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Перезагрузите страницу!"
        )

    if await verify_password(hashed_password=str(user_data.password_hash), password=data.password):
        await delete_me(user_id=user_id)
    return "Ok"

