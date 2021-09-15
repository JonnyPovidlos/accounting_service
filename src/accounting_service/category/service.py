from fastapi import Depends

from accounting_service.database import get_session, Session, update_attrs
from accounting_service.category.models import Category as CategoryORM
from accounting_service.category.schemas import BaseCategory


class CategoryService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_category(self, category_create: BaseCategory) -> CategoryORM:
        category = CategoryORM(**category_create.dict(exclude_unset=True))
        self.session.add(category)
        self.session.commit()
        return category

    def _get(self, category_id: int) -> CategoryORM:
        category = self.session.query(CategoryORM).where(CategoryORM.id == category_id).one()
        return category

    def update_category(self, category_id: int, category_update: BaseCategory) -> CategoryORM:
        category = self._get(category_id)
        update_attrs(category, category_update)
        self.session.commit()
        return category

    def delete_category(self, category_id):
        category = self._get(category_id)
        self.session.delete(category)
        self.session.commit()


