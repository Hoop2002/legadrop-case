from typing import Optional
from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    user_id: str
    username: Optional[str]
    email: EmailStr
    password_hash: Optional[str]
    image: Optional[str]
    balance: Optional[int]
    locale: Optional[str]
    verified: Optional[bool]
    active: Optional[bool]


class UserCreate(BaseModel):
    username: Optional[str]
    email: EmailStr
    password_hash: Optional[str]
    image: Optional[str] = "https://www.legdarop/image/username.jpg"
    balance: Optional[int] = 0
    locale: Optional[str] = "ru"
    verified: Optional[bool] = True
    active: Optional[bool] = True


class UserID(BaseModel):
    user_id: str
