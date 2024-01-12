from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from security.password_functions import verify_password
from security.token_functions import create_user_token
from .functions import get_user_by_username, get_user_by_email
from models import ResponseToken

router = APIRouter()


@router.post("/sign-in", response_model=ResponseToken)
async def user_sign_in(data: OAuth2PasswordRequestForm = Depends()):
    user_data = await get_user_by_username(data.username) or await get_user_by_email(
        data.username
    )

    if user_data is None:
        raise HTTPException(
            detail="Неверный логин", status_code=status.HTTP_400_BAD_REQUEST
        )

    await verify_password(str(user_data.password_hash), data.password)
    token = await create_user_token(user_id=user_data.user_id)
    return {"access_token": token, "token_type": "bearer"}
