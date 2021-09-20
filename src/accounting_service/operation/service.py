import datetime

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func
from sqlalchemy.orm import Query

from accounting_service.category.models import Category
from accounting_service.database import get_session, Session
from accounting_service.operation.models import Operation as OperationORM
from accounting_service.operation.schemas import BaseOperation
from accounting_service.report_utils import ReportRecord, make_date_range
from accounting_service.shop.models import Shop
from exceptions import ForeignKeyConstraintFailed


class OperationService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_operation(self, operation_create: BaseOperation, account_id) -> OperationORM:
        operation = OperationORM(**operation_create.dict(exclude_unset=True), account_id=account_id)
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
                        account_id: int,
                        date_from: datetime.date = None,
                        date_to: datetime.date = None,
                        shops: list[int] = None,
                        categories: list[int] = None,
                        ) -> list[OperationORM]:
        query = self.session.query(OperationORM).where(OperationORM.account_id == account_id)
        query = self._make_limitations(query, date_from, date_to, shops, categories)

        return query.all()

    def get_operations(self,
                       account_id: int,
                       date_from: datetime.date = None,
                       date_to: datetime.date = None,
                       shops: list[int] = None,
                       categories: list[int] = None) -> list[OperationORM]:
        return self._get_operations(account_id, date_from, date_to, shops, categories)

    def _make_report_query(self, account_id, *args, **kwargs) -> Query:
        query = select(
            func.date(OperationORM.date, 'start of month'),
            OperationORM.type,
            Shop.name.label('shop'),
            Category.name.label('category'),
            OperationORM.name,
            func.sum(OperationORM.amount)
        ).join(
            Shop, OperationORM.shop_id == Shop.id
        ).outerjoin(
            Category, OperationORM.category_id == Category.id
        ).where(OperationORM.account_id == account_id)
        query = self._make_limitations(query, *args, **kwargs)
        query = query.group_by(
            func.date(OperationORM.date, 'start of month'),
            OperationORM.type,
            Shop.name,
            Category.name,
            OperationORM.name
        )
        return query

    def get_report(self,
                   account_id,
                   date_from: datetime.date = None,
                   date_to: datetime.date = None,
                   shops: list[int] = None,
                   categories: list[int] = None):
        query = self._make_report_query(account_id=account_id,
                                        date_from=date_from,
                                        date_to=date_to,
                                        shops=shops,
                                        categories=categories)
        report_records = {
            'buy': ReportRecord('Покупки'),
            'sale': ReportRecord('Продажи')
        }
        min_date = None
        max_date = None
        for row in self.session.execute(query).all():
            dict_row = dict(row)
            row_type = dict_row['type'].value
            row_type_name = dict_row['type'].name.lower()
            print(row_type)
            row_date = datetime.date.fromisoformat(dict_row['date']).replace(day=1)
            row_amount = dict_row['sum']
            path = [
                row['shop'],
                row['category'] or 'Без категории',
                row['name']
            ]
            report_records[row_type_name].add_row(path, row_date, row_amount)
            max_date = max(max_date or row_date, row_date)
            min_date = min(min_date or row_date, row_date)

        report_records['time_points'] = make_date_range(min_date, max_date)
        report_records['buy'].make_amounts_per_date(report_records['time_points'])
        return report_records
