from pydantic import RootModel, BaseModel
from typing import List


class RarityCategorySchema(BaseModel):
    name: str


class UserItemSchema(BaseModel):
    id: int
    name: str
    color: str | None
    image: str | None
    rarity_category: RarityCategorySchema

    class Config:
        from_attributes = True


class UserItemsList(RootModel):
    root: List[UserItemSchema]
