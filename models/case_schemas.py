from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, RootModel
from models.item_schemas import AdminItemSchema, ItemRequestSchema


class OpenCaseData(BaseModel):
    item_id: str
    rarity_id: str


class ItemList(BaseModel):
    items: List[OpenCaseData]


class AdminCategorySchema(BaseModel):
    category_id: str
    name: str


class AdminCreateCaseSchema(BaseModel):
    name: str
    category_id: Optional[str]
    image_name: str
    image: str  # base64
    price: float
    case_free: Optional[bool]
    items: List[ItemRequestSchema]


class AdminCaseSchema(BaseModel):
    case_id: str
    name: str
    image: str
    case_id: str
    price: float
    case_free: bool
    created_at: datetime
    category: Optional[AdminCategorySchema]
    # items: Optional[List[AdminItemSchema]]

    class Config:
        from_attributes = True
