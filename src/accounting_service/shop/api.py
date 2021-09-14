from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from accounting_service.database import Session
from accounting_service.shop.models import Shop

router = APIRouter(prefix='/shops')


@router.post('',
             status_code=status.HTTP_201_CREATED)
def create_shop(name: str):
    with Session() as session:
        shop = Shop(name=name)
        session.add(shop)
        session.commit()
        return {
            'id': shop.id,
            'name': shop.name
        }


@router.patch('/{shop_id}',
              status_code=status.HTTP_202_ACCEPTED)
def update_shop(shop_id: int,
                name: str):
    with Session() as session:
        try:
            shop = session.query(Shop).filter(Shop.id == shop_id).one()
        except NoResultFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            shop.name = name
            session.add(shop)
            session.commit()
            return {
                'id': shop.id,
                'name': shop.name
            }


@router.delete('/{shop_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id: int):
    with Session() as session:
        try:
            shop = session.query(Shop).filter(Shop.id == shop_id).one()
        except NoResultFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            session.delete(shop)
            session.commit()
            return {}
