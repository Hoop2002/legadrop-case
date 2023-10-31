from pydantic import BaseModel


class Password(BaseModel):
    password: str


class PasswordGenerator(BaseModel):
    length: int = 8
    uppercase: bool = True
    digits: bool = True
    characters: bool = False
