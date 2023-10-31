from fastapi import APIRouter, HTTPException, status
from typing import Union
from time import time
from email_validator import validate_email, EmailNotValidError
from security.password_functions import password_generator, hash_password
from security.token_functions import create_user_token
from .functions import (
    auth,
    auth_google,
    get_user_by_username,
    get_user_by_email,
    get_user_by_social_id,
)
from models import (
    RequestGoogleAuth,
    UserSignUp,
    GoogleAuth,
    ResponseToken,
    ResponseTokenPassword
)

router = APIRouter()


@router.post("/auth/google", response_model=ResponseTokenPassword)
async def auth_google_(user_data: RequestGoogleAuth):
    try:
        validate_email(user_data.email)
    except EmailNotValidError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный email"
        )
    old_user = await get_user_by_social_id(str(user_data.social_id))
    if old_user:
        access_token = await create_user_token(user_id=str(old_user.user_id))
        return {"access_token": access_token, "token_type": "bearer"}
    if await get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )
    if await get_user_by_username(user_data.username):
        user_data.username = f"{user_data.username}{time()}"
    password = await password_generator()
    hashed_password = await hash_password(password=password)
    created_user = await auth(
        UserSignUp(email=user_data.email, password_hash=hashed_password)
    )
    await auth_google(
        GoogleAuth(user_id=str(created_user.user_id), social_id=user_data.social_id)
    )
    access_token = await create_user_token(user_id=str(created_user.user_id))

    return {"access_token": access_token, "token_type": "bearer", "password": password}
