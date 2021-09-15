from pydantic import BaseModel


class BaseCategory(BaseModel):
    name: str


class Category(BaseCategory):
    id: int

    class Config:
        orm_mode = True
