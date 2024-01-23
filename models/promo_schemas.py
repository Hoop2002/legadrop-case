from datetime import datetime
from enum import Enum
from pydantic import RootModel, BaseModel
from typing import List, Optional


class CodeTypeEnum(str, Enum):
    bonus = 'bonus'
    balance = 'balance'


class PromoCodeRequestSchema(BaseModel):
    name: str
    type_code: CodeTypeEnum
    activations: Optional[str] | None
    to_date: Optional[datetime] | None
    active: bool = True

    class Config:
        from_attributes = True


class PromoCodeResponseSchema(PromoCodeRequestSchema):
    creation_date: datetime


class ListPromoCodesSchema(RootModel):
    root: List[PromoCodeResponseSchema]
