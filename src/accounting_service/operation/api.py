import datetime
from typing import Optional

from fastapi import APIRouter

from accounting_service.database import Session
from accounting_service.operation.models import Operation as OperationORM
from accounting_service.operation.schemas import BaseOperation, Operation

router = APIRouter(prefix='/operations', tags=['operation'])


@router.post('',
             response_model=Operation)
def create_operation(operation_create: BaseOperation):
    with Session() as session:
        # date = datetime.datetime.fromisoformat(date).date()
        operation = OperationORM(**operation_create.dict(exclude_unset=True))
        session.add(operation)
        session.commit()
        return {
            'id': operation.id,
            'type': operation.type,
            'date': operation.date,
            'shop_id': operation.shop_id,
            'category_id': operation.category_id,
            'name': operation.name,
            'price': operation.price,
            'amount': operation.amount
        }
