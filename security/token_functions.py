# Импорт сторонних библиотек
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError

from datetime import datetime, timedelta
from dotenv import load_dotenv

# Импорт модулей приложения
from models import TokenData, RequestAdminID, UserID

import os

# Загрузка переменных окружения
load_dotenv()


ADMINSECRET = os.getenv("ADMINSECRET")
USERSECRET = os.getenv("USERSECRET")
ALGORITHM = "HS256"
TOKEN_EXP = 7200.0
KID = "1"

admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/sign-in")
user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign-in")


async def create_admin_token(admin_id: str) -> str:
    payload = {
        "sub": admin_id,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXP),
        "iss": "legadrop.org",
    }
    headers = {"kid": KID}
    try:
        token = jwt.encode(payload, ADMINSECRET, algorithm=ALGORITHM, headers=headers)  # type: ignore
        return token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Побробуйте позже"
        )


async def verify_admin(token: str = Depends(admin_oauth2_scheme)) -> RequestAdminID:
    try:
        payload = jwt.decode(token, key=ADMINSECRET, algorithms=[ALGORITHM])  # type: ignore
        token_data = TokenData(**payload)
        admin_id = token_data.sub
        response = RequestAdminID(admin_id=admin_id)
        return response
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен просрочен"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен"
        )


async def create_user_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXP),
        "iss": "legadrop.org",
    }
    headers = {"kid": KID}
    try:
        token = jwt.encode(payload, USERSECRET, algorithm=ALGORITHM, headers=headers)
        return token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Побробуйте позже"
        )


async def verify_user(token: str = Depends(user_oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, key=USERSECRET, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        return token_data.sub
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен просрочен"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен"
        )
