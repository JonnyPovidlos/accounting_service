import datetime
import enum
from typing import Optional

from sqlalchemy import Column, Integer, Enum, Date, Numeric, ForeignKey, String
from sqlalchemy.orm import relationship

from accounting_service.database import Base


class OperationType(str, enum.Enum):
    BUY = 'buy'
    SALE = 'sale'


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(OperationType), nullable=False)
    date = Column(Date, nullable=False)
    shop_id = Column(ForeignKey('shop.id', ondelete='CASCADE', name='shop_key'), nullable=False)
    category_id = Column(ForeignKey('category.id', ondelete='CASCADE', name='category_key'))
    name = Column(String, nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
    account_id = Column(ForeignKey('account.id', name='account_key'), nullable=False)

    shop = relationship('Shop')
    category = relationship('Category')

    def __init__(self,
                 type: OperationType,
                 date: datetime,
                 shop_id: int,
                 name: str,
                 price: float,
                 amount: float,
                 account_id: int,
                 category_id: Optional[int] = None):
        self.type = type
        self.date = date
        self.shop_id = shop_id
        self.name = name
        self.price = price
        self.amount = amount
        self.category_id = category_id
        self.account_id = account_id

    def __repr__(self):
        return f'<Operation {self.id}>'

