from pydantic import BaseModel


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