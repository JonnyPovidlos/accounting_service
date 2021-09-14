import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from accounting_service.database import Session
from accounting_service.operation.models import Operation, TypeOperation

router = APIRouter(prefix='/operations', tags=['operation'])


@router.post('')
def create_operation(
        type: TypeOperation,
        date: str,
        shop_id: int,
        price: float,
        amount: float,
        category_id: Optional[int] = None
):
    with Session() as session:
        date = datetime.datetime.fromisoformat(date).date()
        operation = Operation(type=type.name,
                              date=date,
                              shop_id=shop_id,
                              price=price,
                              amount=amount,
                              category_id=category_id)
        session.add(operation)
        session.commit()
        return {
            'id': operation.id,
            'type': operation.type,
            'date': operation.date,
            'shop_id': operation.shop_id,
            'category_id': operation.category_id,
            'price': operation.price,
            'amount': operation.amount
        }
