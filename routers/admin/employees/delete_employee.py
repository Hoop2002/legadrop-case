from fastapi import APIRouter, Depends, HTTPException, status
from security import verify_admin

# from ..permissions.functions import has_permission
from .functions import delete_employee
from models import ReponseAdminDelete, RequestAdminDelete, RequestAdminID


router = APIRouter()


ROLE_MANAGEMENT_PERMISSION = "Создание сотрудников"

# @router.delete("/employee", response_model=ReponseAdminDelete)
# async def delete_employee_(data: RequestAdminDelete, auth: RequestAdminID = Depends(verify_admin)):
#     if not await has_permission(auth.admin_id, ROLE_MANAGEMENT_PERMISSION):
#         raise HTTPException(status_code=403, detail="У вас нет прав")
#     deleted_employee = await delete_employee(data.admin_id)
#     if deleted_employee:
#         return HTTPException(status_code=status.HTTP_200_OK, detail="Сотрудник успешно удален")
#     else:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Сотрудник не найден")


@router.delete("/employee", response_model=ReponseAdminDelete)
async def delete_employee_(
    data: RequestAdminDelete, admin: str = Depends(verify_admin)
):
    deleted_employee = await delete_employee(data.admin_id)
    if deleted_employee:
        return HTTPException(
            status_code=status.HTTP_200_OK, detail="Сотрудник успешно удален"
        )
    else:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Сотрудник не найден"
        )
