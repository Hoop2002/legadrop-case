from typing import Optional, List
from pydantic import BaseModel, EmailStr


class OpenCaseData(BaseModel):
    item_id: str
    rarity_id: str





class ItemList(BaseModel):
    items: List[OpenCaseData]
