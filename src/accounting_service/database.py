from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (Column,
                        Integer,
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


def get_session() -> Session:
    with Session() as session:
        yield session


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

from accounting_service.category.models import Category # noqa
from accounting_service.operation.models import Operation # noqa
from accounting_service.shop.models import Shop # noqa
