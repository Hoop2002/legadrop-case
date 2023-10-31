from fastapi import APIRouter, HTTPException, status
from .functions import create_role, get_role_by_name
from models import RequestRoleCreate

router = APIRouter()


@router.post("/role")
async def create_role_(data: RequestRoleCreate):
    if await get_role_by_name(data.role) is None:
        role_data = await create_role(data.role)
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=f"Дольжность '{role_data.name}' успешна создана",
        )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Роль {data.role} уже существует.",
    )
