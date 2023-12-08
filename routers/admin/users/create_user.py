from fastapi import APIRouter
from models import RequestUserCreate, UserCreate
from .functions import create_user

router = APIRouter()


@router.post("/create_user")
async def create_user_route(user: RequestUserCreate):
    user_data = user.model_dump()
    user_data["password_hash"] = user_data.pop("password")
    user_data = UserCreate(**user_data)
    return await create_user(user_data)
