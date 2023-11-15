from typing import Optional, List
from pydantic import BaseModel, EmailStr


class OpenCaseData(BaseModel):
    item_id: str
    rarity_id: str

class User__data(BaseModel):
    uid: str


class ItemList(BaseModel):
    user: User__data
    items: List[OpenCaseData]