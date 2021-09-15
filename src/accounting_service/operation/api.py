from fastapi import Query
import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from accounting_service.operation.schemas import BaseOperation, Operation
from accounting_service.operation.service import OperationService

router = APIRouter(prefix='/operations', tags=['operation'])


@router.post('',
             response_model=Operation)
def create_operation(operation_create: BaseOperation,
                     service: OperationService = Depends()):
    operation = service.create_operation(operation_create)
    return operation


@router.get('',
            response_model=list[Operation])
def get_operations(
        date_from: Optional[datetime.date] = None,
        date_to: Optional[datetime.date] = None,
        shops: Optional[list[int]] = Query(None),
        categories: Optional[list[int]] = Query(None),
        service: OperationService = Depends()):
    operations = service.get_operations(date_from, date_to, shops, categories)
    return operations
