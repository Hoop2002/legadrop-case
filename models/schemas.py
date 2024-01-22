from pydantic import RootModel, BaseModel
from typing import List


class RarityCategorySchema(BaseModel):
    name: str


class ItemRequestSchema(BaseModel):
    id: int


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
