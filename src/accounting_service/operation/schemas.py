import datetime
from typing import Optional

from pydantic import BaseModel

from accounting_service.operation.models import OperationType


class BaseOperation(BaseModel):
    type: OperationType
    date: datetime.date
    shop_id: int
    category_id: Optional[int] = None
    name: str
    price: float
    amount: float


class Operation(BaseOperation):
    id: int

    class Config:
        orm_mode = True
