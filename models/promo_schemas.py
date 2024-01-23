from datetime import datetime
from enum import Enum
from pydantic import RootModel, BaseModel
from typing import List, Optional

from utils import id_generator


class CodeTypeEnum(str, Enum):
    bonus = "bonus"
    balance = "balance"


class PromoCodeRequestSchema(BaseModel):
    name: str
    type_code: CodeTypeEnum
    activations: Optional[str] | None
    to_date: Optional[datetime] | None
    active: bool = True
    code_data: str = id_generator

    class Config:
        from_attributes = True


class PromoCodeResponseSchema(PromoCodeRequestSchema):
    creation_date: datetime
    code_data: str


class PromoCodeSchema(BaseModel):
    name: str
    active: bool = True
    code_data: str

    class Config:
        from_attributes = True


class ListPromoCodesSchema(RootModel):
    root: List[PromoCodeSchema]
