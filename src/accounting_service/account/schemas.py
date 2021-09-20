from pydantic import BaseModel


class BaseAccount(BaseModel):
    username: str
    email: str


class CreateAccount(BaseAccount):
    password: str


class Account(BaseAccount):
    id: int

    class Config:
        orm_mode = True


class LoginAccount(BaseModel):
    username: str
    password: str

