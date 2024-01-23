from datetime import datetime
from enum import Enum
from pydantic import RootModel, BaseModel
from typing import List, Optional


class CodeTypeEnum(str, Enum):
    bonus = "bonus"
    balance = "balance"


class PromoCodeRequestSchema(BaseModel):
    name: str
    summ: float
    active: bool = True
    code_data: Optional[str] = None
    type_code: CodeTypeEnum
    limit_activations: Optional[int] = None
    to_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class PromoCodeResponseSchema(PromoCodeRequestSchema):
    id: int
    activations: Optional[int] = None
    creation_date: datetime
    code_data: str


class PromoCodeSchema(BaseModel):
    id: int
    name: str
    active: bool = True
    code_data: str

    class Config:
        from_attributes = True


class ListPromoCodesSchema(RootModel):
    root: List[PromoCodeSchema]
