from sqlalchemy import Integer, String, Column

from accounting_service.database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Category {self.id}>'
