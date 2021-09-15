import datetime
import enum
from typing import Optional

from sqlalchemy import Column, Integer, Enum, Date, Numeric, ForeignKey, String

from accounting_service.database import Base


class TypeOperation(str, enum.Enum):
    BUY = 'buy'
    SALE = 'sale'


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(TypeOperation), nullable=False)
    date = Column(Date, nullable=False)
    shop_id = Column(ForeignKey('shop.id', ondelete='CASCADE', name='shop_key'), nullable=False)
    category_id = Column(ForeignKey('category.id', ondelete='CASCADE', name='category_key'))
    name = Column(String, nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)

    def __init__(self,
                 type: TypeOperation,
                 date: datetime,
                 shop_id: int,
                 name: str,
                 price: float,
                 amount: float,
                 category_id: Optional[int] = None):
        self.type = type
        self.date = date
        self.shop_id = shop_id
        self.name = name
        self.price = price
        self.amount = amount
        self.category_id = category_id

    def __repr__(self):
        return f'<Operation {self.id}>'

