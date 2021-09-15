from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from starlette import status

from accounting_service.database import Session
from accounting_service.shop.models import Shop as ShopORM
from accounting_service.shop.schemas import Shop, BaseShop

router = APIRouter(prefix='/shops', tags=['shop'])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=Shop)
def create_shop(shop_create: BaseShop):
    with Session() as session:
        shop = ShopORM(**shop_create.dict(exclude_unset=True))
        session.add(shop)
        session.commit()
        return {
            'id': shop.id,
            'name': shop.name
        }


@router.patch('/{shop_id}',
              status_code=status.HTTP_202_ACCEPTED,
              response_model=Shop)
def update_shop(shop_id: int,
                shop_update: BaseShop):
    with Session() as session:
        try:
            shop = session.query(ShopORM).filter(ShopORM.id == shop_id).one()
        except NoResultFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            for attr, val in shop_update.dict(exclude_unset=True).items():
                setattr(shop, attr, val)
            session.commit()
            return shop


@router.delete('/{shop_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id: int):
    with Session() as session:
        try:
            shop = session.query(ShopORM).filter(ShopORM.id == shop_id).one()
        except NoResultFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        else:
            session.delete(shop)
            session.commit()
            return {}
