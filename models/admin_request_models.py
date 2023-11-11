from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List, Any


class RequestCreateCategory(BaseModel):
    name: str


class RequestCategory(BaseModel):
    category_id: str


class RequestCategoryName(BaseModel):
    name: str


class RequestCategoryUpdate(BaseModel):
    category_id: str
    name: str


class RequestCategoryDelete(BaseModel):
    category_id: str


class RequestCreateCase(BaseModel):
    name: str
    category_id: str


class RequestCase(BaseModel):
    case_id: str


class RequestCaseName(BaseModel):
    name: str


class RequestCaseUpdate(BaseModel):
    case_id: str
    name: str


class RequestCaseDelete(BaseModel):
    case_id: str


class RequestCreateItem(BaseModel):
    name: str
    image: str


class RequestItem(BaseModel):
    item_id: str


class RequestItemName(BaseModel):
    name: str


class RequestItemUpdate(BaseModel):
    item_id: str
    name: str
    image: str


class RequestItemDelete(BaseModel):
    item_id: str


class RequestAddCaseItem(BaseModel):
    case_id: str
    item_id: str


class RequestCaseItem(BaseModel):
    case_id: str
    item_id: str


class RequestCaseItems(BaseModel):
    case_id: str


class RequestCaseItemDelete(BaseModel):
    case_id: str
    item_id: str



class Request(BaseModel):
    data: Dict[str, Any]


class RequstAdminCreate(BaseModel):
    username: str = "admin"
    first_name: Optional[str] = "Ivan"
    last_name: Optional[str] = "Ivanov"
    email: EmailStr
    password: str = "0000"


class RequestAdminID(BaseModel):
    admin_id: str


class RequestAssignRole(BaseModel):
    username: str
    role: str


class RequestAssignPermission(BaseModel):
    role_name: str
    permissions_names: List[str]


class RequestRolePermissions(BaseModel):
    role_name: str


class RequestAdminDelete(BaseModel):
    admin_id: str


class RequestRoleCreate(BaseModel):
    role: str


class RequestRoleID(BaseModel):
    role: str


class RequestRoleName(BaseModel):
    role_id: str


class RequestPermissionCreate(BaseModel):
    permission: str


class RequestPermissionID(BaseModel):
    permission: str


class RequestPermission(BaseModel):
    permission_id: str


class RequestUserSignUp(BaseModel):
    email: EmailStr
    password: str


class RequestGoogleAuth(BaseModel):
    social_id: int = 1234567890
    username: str = "username"
    email: EmailStr
    image: str = "https://www.legdarop.org/image/user.jpg"
    locale: str = "ru"


class RequestUserCreate(BaseModel):
    username: Optional[str]
    email: EmailStr
    password: str
    image: str = "https://www.legdarop.org/image/user.jpg"
    locale: Optional[str] = "ru"

