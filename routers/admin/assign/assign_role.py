from ast import Await
from fastapi import APIRouter, Depends, HTTPException, status
from .functions import assign_role, get_admin_role
from models import RequestAssignRole


router = APIRouter()

@router.post("/assign/role")
async def assign_role_(data: RequestAssignRole):
    if not await get_admin_role(username=data.username):
        admin, role = await assign_role(data.username, data.role)
        return HTTPException(status_code=status.HTTP_201_CREATED, detail=f"Должность '{role.name}' успешно назначено сотруднику {admin.username}")