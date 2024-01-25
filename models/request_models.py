from pydantic import BaseModel
from typing import Optional, List


class RequestUpdateMeUsername(BaseModel):
    username: str


class RequestUpdateMeEmail(BaseModel):
    email: str


class RequestUpdateMeLocale(BaseModel):
    locale: str


class RequestChangePassword(BaseModel):
    old_password: str
    new_password: str


class RequestDeleteMe(BaseModel):
    password: str


# todo к удалению
class ListItems(BaseModel):
    item_id: str


class AddItemsInOneCase(BaseModel):
    case_id: str
    items: List[ListItems]


class RarityCategoryUPD(BaseModel):
    rarity_id: str
    category_percent: str
    name: str


class MoogoldOutputOfTheItem(BaseModel):
    genshin_user_id: str
    item_id: str


class MoogoldOutputOfTheItems(BaseModel):
    genshin_user_id: str
    items: List[ListItems]


class PurchaseMoogoldOutputOfTheItems(BaseModel):
    itemfs_id: str


class OutputAllItemF(BaseModel):
    user_id: str
    genshin_user_id: str
    outputs: List[ListItems]
