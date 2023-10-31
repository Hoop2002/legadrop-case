from pydantic import BaseModel

class AssignRoleData(BaseModel):
    admin_id: str
    role_id: str
