from fastapi import APIRouter, HTTPException, status, Depends
from models import RequestChangePassword
from security.token_functions import verify_user
from security.password_functions import verify_password
from .functions import get_me, update_password

router = APIRouter()

@router.put("/user/password")
async def change_password(
    data: RequestChangePassword, user_id: str = Depends(verify_user)
):
    user_data = await get_me(user_id)
    
    if not user_data:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Перезагрузите страницу!"
        )

    if await verify_password(hashed_password=str(user_data.password_hash), password=data.old_password):
        return await update_password(user_id, data.new_password)
