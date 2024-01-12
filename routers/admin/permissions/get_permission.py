from fastapi import APIRouter
from .functions import get_permission
from models import RequestPermission, ResponsePermission

router = APIRouter()


@router.get("/permission", response_model=ResponsePermission)
async def get_permission_(data: RequestPermission):
    permission = await get_permission(data.permission_id)
    return permission
