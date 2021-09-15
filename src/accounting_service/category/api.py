from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from accounting_service.database import Session
from accounting_service.category.models import Category as CategoryORM
from accounting_service.category.schemas import BaseCategory, Category

router = APIRouter(prefix='/categories', tags=['category'])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=Category)
def create_category(category_create: BaseCategory):
    with Session() as session:
        category = CategoryORM(**category_create.dict(exclude_unset=True))
        session.add(category)
        session.commit()
        return {
            'id': category.id,
            'name': category.name
        }


@router.patch('/{category_id}',
              status_code=status.HTTP_202_ACCEPTED,
              response_model=Category)
def update_category(category_id: int,
                    category_update: BaseCategory):
    with Session() as session:
        try:
            category = session.query(CategoryORM).filter(CategoryORM.id == category_id).one()
        except NoResultFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            for attr, val in category_update.dict(exclude_unset=True).items():
                setattr(category, attr, val)
            # session.commit()
            return {
                'id': category.id,
                'name': category.name
            }


@router.delete('/{category_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_category(shop_id: int):
    with Session() as session:
        try:
            shop = session.query(CategoryORM).filter(CategoryORM.id == shop_id).one()
        except NoResultFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            session.delete(shop)
            session.commit()
            return {}
