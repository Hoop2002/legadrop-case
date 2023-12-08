from fastapi import APIRouter, Depends, HTTPException, status
from security import hash_password, verify_admin
from .functions import create_employee, get_by_email, get_by_username

# from ..permissions.functions import has_permission
from models import AdminCreate, RequstAdminCreate, AdminData

router = APIRouter()

ROLE_MANAGEMENT_PERMISSION = "Создание сотрудников"

# @router.post("/employee")
# async def create_employee_route(data: RequstAdminCreate, auth: RequestAdminID = Depends(verify_admin)):
#     if not await has_permission(auth.admin_id, ROLE_MANAGEMENT_PERMISSION):
#         raise HTTPException(status_code=403, detail="У вас нет прав")
#     exist_employee = await get_by_email(data.email)
#     if exist_employee:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким адресом электронной почты уже существует")
#     exist_employee = await get_by_username(data.username)
#     if exist_employee:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким именем пользователя уже существует")
#     admin_data = data.model_dump()
#     admin_data.update({"password_hash": await hash_password(admin_data.pop("password"))})
#     admin_data = AdminCreate(**admin_data)
#     created_admin = await create_employee(admin_data)
#     return created_admin


@router.post("/employee", response_model=AdminData)
async def create_employee_(data: RequstAdminCreate):
    exist_employee = await get_by_email(data.email)
    if exist_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким адресом электронной почты уже существует",
        )
    exist_employee = await get_by_username(data.username)
    if exist_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем пользователя уже существует",
        )
    admin_data = data.model_dump()
    admin_data.update(
        {"password_hash": await hash_password(admin_data.pop("password"))}
    )
    admin_data = AdminCreate(**admin_data)
    created_admin = await create_employee(admin_data)
    return created_admin
    # return HTTPException(status_code=status.HTTP_201_CREATED, detail="Сотрудник успешно создан")
