from fastapi import Query, status, HTTPException
import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from accounting_service.account.schemas import Account
from accounting_service.operation.schemas import BaseOperation, Operation
from accounting_service.operation.service import OperationService
from accounting_service.report_utils import parse_list_shops, parse_list_categories
from exceptions import ForeignKeyConstraintFailed, NoResultFoundCustom
from accounting_service.auth import get_current_account

router = APIRouter(prefix='/operations', tags=['operation'])


@router.post('',
             response_model=Operation,
             status_code=status.HTTP_201_CREATED)
def create_operation(operation_create: BaseOperation,
                     service: OperationService = Depends(),
                     current_account: Account = Depends(get_current_account)):
    try:
        operation = service.create_operation(operation_create, current_account.id)
        return operation
    except ForeignKeyConstraintFailed:
        raise HTTPException(status.HTTP_409_CONFLICT)
    except NoResultFoundCustom:
        raise HTTPException(status.HTTP_409_CONFLICT)


@router.get('',
            response_model=list[Operation])
def get_operations(
        date_from: Optional[datetime.date] = None,
        date_to: Optional[datetime.date] = None,
        shops: Optional[list[int]] = Depends(parse_list_shops),
        categories: Optional[list[int]] = Depends(parse_list_categories),
        service: OperationService = Depends(),
        current_account: Account = Depends(get_current_account)):
    operations = service.get_operations(current_account.id, date_from, date_to, shops, categories)
    return operations


@router.get('/report')
def get_report(date_from: Optional[datetime.date] = None,
               date_to: Optional[datetime.date] = None,
               shops: Optional[list[int]] = Depends(parse_list_shops),
               categories: Optional[list[int]] = Depends(parse_list_categories),
               service: OperationService = Depends(),
               current_account: Account = Depends(get_current_account)):
    report = service.get_report(current_account.id, date_from, date_to, shops, categories)
    return {
        'time_points': report['time_points'],
        'buy': report['buy'].as_dict(),
        'sale': report['sale'].as_dict()
    }
