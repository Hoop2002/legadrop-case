from pydantic import BaseModel, EmailStr
from typing import Union


class AdminSignIn(BaseModel):
    username: str
    password: str


class UserSignUp(BaseModel):
    email: EmailStr
    password_hash: str


class UserSignIn(BaseModel):
    login: Union[str, EmailStr]
    password: str


class GoogleAuth(BaseModel):
    user_id: str
    provider: str = "google"
    social_id: int
