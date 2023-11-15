from fastapi import APIRouter, HTTPException, status, Depends

from fastapi.security import OAuth2PasswordRequestForm
from security.password_functions import verify_password
from security.token_functions import create_admin_token
from ..employees.functions import get_by_username, get_by_email
from models import ResponseToken

router = APIRouter()

from pydantic import BaseModel


class ResponseToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/sign-in", response_model = ResponseToken)
async def admin_sign_in(data: OAuth2PasswordRequestForm = Depends()):
	admin_data = await get_by_username(data.username) or await get_by_email(data.username)
	
	if admin_data is None:
		raise HTTPException(detail="Неверное имя пользователя или почта", status_code = status.HTTP_400_BAD_REQUEST)
	
	admin_id = admin_data.admin_id
	password_hash = admin_data.password_hash


	await verify_password(password_hash, data.password)
	token = await create_admin_token(admin_id)
	return {"access_token": token, "token_type": "bearer"}
