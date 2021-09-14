import enum
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (Column,
                        Integer,
                        Enum,
                        DateTime,
                        Numeric,
                        String,
                        create_engine,
                        event,
                        engine)


@event.listens_for(engine.Engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()


__engine = create_engine(url='sqlite:///test.sqlite',
                         future=True,
                         connect_args={'check_same_thread': False})
Session = sessionmaker(bind=__engine,
                       future=True)
Base = declarative_base()


class TypeOperation(str, enum.Enum):
    BUY = 'byy'
    SALE = 'sale'


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(TypeOperation), nullable=False)
    date = Column(DateTime, nullable=False)
    shop_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False)
