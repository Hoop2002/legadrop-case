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

class ListItems(BaseModel):
    item_id: str


class CreateCases(BaseModel):
    name: str
    category: str
    image_name: str
    image: str #base64
    items: List[ListItems]

class AddItemsInOneCase(BaseModel):
    case_id: str
    items: List[ListItems]