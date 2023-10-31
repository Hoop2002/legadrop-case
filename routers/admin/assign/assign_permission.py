from fastapi import APIRouter, HTTPException, status
from .functions import assign_permission
from models import RequestAssignPermission


router = APIRouter()

@router.post("/assign/permission")
async def assign_permission_(request: RequestAssignPermission):
    try:
        await assign_permission(request.role_name, request.permissions_names)
        return HTTPException(status_code=status.HTTP_201_CREATED, detail="Разрешения роли успешно назначены!")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))