from fastapi import APIRouter
from models import PasswordGenerator
from security import password_generator

router = APIRouter()

@router.post("/generator/password")
async def generator_password(parametrs: PasswordGenerator):
    password = await password_generator(parametrs.length, parametrs.uppercase, parametrs.digits, parametrs.characters)
    
    return {"password": password }