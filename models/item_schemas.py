from datetime import datetime
from pydantic import RootModel, BaseModel, Field
from typing import List


class RarityCategorySchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class AdminRarityCategorySchema(RarityCategorySchema):
    id: int
    name: str
    category_id: str
    category_percent: float = Field(le=1)
    ext_id: str


class ItemRequestSchema(BaseModel):
    item_id: str


class ItemSchema(ItemRequestSchema):
    name: str
    cost: float | None
    cost_in_rubles: float | None
    color: str | None
    image: str | None
    rarity_category: RarityCategorySchema

    class Config:
        from_attributes = True


class ItemsListSchema(RootModel):
    root: List[ItemSchema]


class UserItemsSchema(BaseModel):
    id: int
    # count: int
    item: ItemSchema

    class Config:
        from_attributes = True


class UserItemsListSchema(RootModel):
    root: List[UserItemsSchema]


class AdminItemSchema(ItemSchema):
    item_id: str
    sale: bool
    created_at: datetime
    step_down_factor: float
    rarity_category: AdminRarityCategorySchema
