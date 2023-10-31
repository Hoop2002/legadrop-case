from typing import Optional, List
from pydantic import BaseModel, EmailStr

class AdminMe(BaseModel):
    admin_id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    image: str

class AdminData(BaseModel):
    admin_id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    image: str


class AdminDataList(BaseModel):
    employees: List[AdminData]

class AdminCreate(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password_hash: str
    image: Optional[str] = "http://localhost:8000/pictures/user.jpg"

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None
    image: Optional[str] = None

