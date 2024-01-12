from pydantic import BaseModel


class PermissionData(BaseModel):
    permission_id: str
    permission: str
