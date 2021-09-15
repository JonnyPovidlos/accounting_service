from fastapi import Depends

from accounting_service.database import get_session, Session, update_attrs
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
