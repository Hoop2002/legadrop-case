from pydantic import BaseModel


class AdminRoleData(BaseModel):
    admin_id: str
    role_id: str

