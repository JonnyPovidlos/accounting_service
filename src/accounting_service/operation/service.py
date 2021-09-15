import datetime

from fastapi import Depends

from accounting_service.database import get_session, Session
from accounting_service.operation.models import Operation as OperationORM
from accounting_service.operation.schemas import BaseOperation


class OperationService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_operation(self, operation_create: BaseOperation) -> OperationORM:
        operation = OperationORM(**operation_create.dict(exclude_unset=True))
        self.session.add(operation)
        self.session.commit()
        return operation

    def _get_operations(self,
                        date_from: datetime.date = None,
                        date_to: datetime.date = None,
                        shops: list[int] = None,
                        categories: list[int] = None) -> list[OperationORM]:
        query = self.session.query(OperationORM)
        if date_from:
            query = query.where(OperationORM.date >= date_from)
        if date_to:
            query = query.where(OperationORM.date <= date_to)
        if shops:
            query = query.where(OperationORM.shop_id.in_(shops))
        if categories:
            query = query.where(OperationORM.category_id.in_(categories))
        return query.all()

    def get_operations(self,
                       date_from: datetime.date = None,
                       date_to: datetime.date = None,
                       shops: list[int] = None,
                       categories: list[int] = None):
        return self.get_operations(date_from, date_to, shops, categories)
