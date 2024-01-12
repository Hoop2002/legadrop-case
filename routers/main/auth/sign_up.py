from fastapi import APIRouter, HTTPException, status
from email_validator import validate_email, EmailNotValidError

from security.password_functions import hash_password
from security.token_functions import create_user_token
from .functions import get_user_by_email, auth
from models import RequestUserSignUp, UserSignUp, ResponseToken

router = APIRouter()


@router.post("/sign-up", response_model=ResponseToken)
async def user_sign_up(user_data: RequestUserSignUp):
    try:
        validate_email(user_data.email)
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный email"
        )

    if await get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    hashed_password = await hash_password(user_data.password)
    created_user = await auth(
        UserSignUp(email=user_data.email, password_hash=hashed_password)
    )
    access_token = await create_user_token(user_id=str(created_user.user_id))

    return {"access_token": access_token, "token_type": "bearer"}
