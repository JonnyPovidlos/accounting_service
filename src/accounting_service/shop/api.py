from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from accounting_service.auth import get_current_account
from accounting_service.shop.schemas import Shop, BaseShop
from accounting_service.shop.service import ShopService
from exceptions import NoResultFoundCustom
from accounting_service.account.schemas import Account

router = APIRouter(prefix='/shops', tags=['shop'])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=Shop)
def create_shop(shop_create: BaseShop,
                service: ShopService = Depends(),
                current_account: Account = Depends(get_current_account)):
    shop = service.create_shop(shop_create, current_account.id)
    return shop


@router.patch('/{shop_id}',
              status_code=status.HTTP_202_ACCEPTED,
              response_model=Shop)
def update_shop(shop_id: int,
                shop_update: BaseShop,
                service: ShopService = Depends(),
                current_account: Account = Depends(get_current_account)):
    try:
        shop = service.update_shop(shop_id, shop_update, current_account.id)
        return shop
    except NoResultFoundCustom:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete('/{shop_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id: int,
                service: ShopService = Depends(),
                current_account: Account = Depends(get_current_account)):
    try:
        service.delete_shop(shop_id, current_account.id)
        return {}
    except NoResultFoundCustom:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
