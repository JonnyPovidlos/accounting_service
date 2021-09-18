from pydantic import BaseModel


class BaseAccount(BaseModel):
    username: str
    email: str


class CreateAccount(BaseAccount):
    password: str


class Account(BaseAccount):
    id: str

    class Config:
        orm_mode = True
