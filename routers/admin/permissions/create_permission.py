from fastapi import APIRouter
from .functions import create_permission
from models import RequestPermissionCreate, ResponsePermission

router = APIRouter()


@router.post("/permission", response_model=ResponsePermission)
async def create_permission_(data: RequestPermissionCreate):
    permission = data.permission
    response = await create_permission(permission)
    return response
