from pydantic import BaseModel


class BaseShop(BaseModel):
    name: str


class Shop(BaseShop):
    id: int

    class Config:
        orm_mode = True
