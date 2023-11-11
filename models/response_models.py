from pydantic import BaseModel, EmailStr
from typing import Dict, Any, List
from datetime import datetime


class ResponceCategory(BaseModel):
    id: int
    category_id: str
    name: str


class ResponceCase(BaseModel):
    id: int
    case_id: str
    name: str
    image: str
    category_id: str
    created_at: datetime
    category: ResponceCategory


class ResponseCategories(BaseModel):
    categories: List[ResponceCategory]


class ResponseItem(BaseModel):
    id: int
    item_id: str
    name: str
    cost: int
    gem_cost: int
    color: str
    image: str
    created_at: datetime
    rarity_id: str
    compound: list
    cost_in_rubles: str
    step_down_factor: float
    

class ResponseItems(BaseModel):
    items: List[ResponseItem]




class ResponseError(BaseModel):
    error: str


class ResponseData(BaseModel):
    deteil: str
    data: Dict[str, Any]


class ResponseToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResponseTokenPassword(BaseModel):
    access_token: str
    token_type: str = "bearer"
    password: str


class ResponseRole(BaseModel):
    role_id: str
    role: str


class ResponseRoles(BaseModel):
    roles: List[str] = ["admin", "user"]


class ResponseCreateRole(BaseModel):
    role_id: str
    role: str


class ResponceAssignRole(BaseModel):
    admin_id: str
    role_id: str


class ResponsePermission(BaseModel):
    permission_id: str
    permission: str


class ResponsePermissions(BaseModel):
    permissions: List[str] = ["create_magic, do_bankrupt"]


class ResponceAssignPermission(BaseModel):
    admin_id: str
    permission_id: str


# Other responses
class ResponseAdministrators(BaseModel):
    employees: List[str] = ["admin", "user"]

class ResponseAdministrator(BaseModel):
    admin_id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    image: str
    

class ReponseAdminDelete(BaseModel):
    deteil: str = "Сотрудник успешно удален"
