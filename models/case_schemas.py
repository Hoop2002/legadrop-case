from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, RootModel, Base64Str, Base64Bytes
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
    items: List[ItemRequestSchema]


class AdminCaseSchema(AdminCreateCaseSchema):
    case_id: str
    created_at: datetime
    category: AdminItemSchema
    items: AdminItemSchema
