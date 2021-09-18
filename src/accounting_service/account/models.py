from sqlalchemy import Column, Integer, String

from accounting_service.database import Base


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)