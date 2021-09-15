import datetime

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from sqlalchemy.orm import Query

from accounting_service.category.models import Category
from accounting_service.database import get_session, Session
from accounting_service.operation.models import Operation as OperationORM
from accounting_service.operation.schemas import BaseOperation
from accounting_service.shop.models import Shop
from exceptions import ForeignKeyConstraintFailed


class OperationService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_operation(self, operation_create: BaseOperation) -> OperationORM:
        operation = OperationORM(**operation_create.dict(exclude_unset=True))
        self.session.add(operation)
        try:
            self.session.commit()
            return operation
        except IntegrityError:
            raise ForeignKeyConstraintFailed

    @staticmethod
    def _make_limitations(query: Query,
                          date_from: datetime.date = None,
                          date_to: datetime.date = None,
                          shops: list[int] = None,
                          categories: list[int] = None) -> Query:
        if date_from:
            query = query.where(OperationORM.date >= date_from)
        if date_to:
            query = query.where(OperationORM.date <= date_to)
        if shops:
            query = query.where(OperationORM.shop_id.in_(shops))
        if categories:
            query = query.where(OperationORM.category_id.in_(categories))
        return query

    def _get_operations(self,
                        date_from: datetime.date = None,
                        date_to: datetime.date = None,
                        shops: list[int] = None,
                        categories: list[int] = None) -> list[OperationORM]:
        query = self.session.query(OperationORM)
        query = self._make_limitations(query, date_from, date_to, shops, categories)

        return query.all()

    def get_operations(self,
                       date_from: datetime.date = None,
                       date_to: datetime.date = None,
                       shops: list[int] = None,
                       categories: list[int] = None) -> list[OperationORM]:
        return self._get_operations(date_from, date_to, shops, categories)

    def get_report(self,
                   date_from: datetime.date = None,
                   date_to: datetime.date = None,
                   shops: list[int] = None,
                   categories: list[int] = None):
        query = select(
            func.date(OperationORM.date, 'start of month'),
            OperationORM.type,
            Shop.name,
            Category.name,
            OperationORM.name,
            func.sum(OperationORM.amount)
        ).join(
            Shop, OperationORM.shop_id == Shop.id
        ).outerjoin(
            Category, OperationORM.category_id == Category.id
        )
        query = self._make_limitations(query, date_from, date_to, shops, categories)
        query = query.group_by(
            func.date(OperationORM.date, 'start of month'),
            OperationORM.type,
            Shop.name,
            Category.name,
            OperationORM.name
        )
        rows = self.session.execute(query).all()
        for row in rows:
            print(dict(row))
