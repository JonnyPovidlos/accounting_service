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
