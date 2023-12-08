from pydantic import BaseModel


class TokenData(BaseModel):
    sub: str
    exp: int
    iss: str
