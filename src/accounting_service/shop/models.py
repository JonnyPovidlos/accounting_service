from sqlalchemy import Integer, String, Column, ForeignKey

from accounting_service.database import Base


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    account_id = Column(ForeignKey('account.id', name='account_key'), nullable=False)

    def __init__(self, name: str, account_id: int):
        self.name = name
        self.account_id = account_id

    def __repr__(self):
        return f'<Shop: {self.id}>'
