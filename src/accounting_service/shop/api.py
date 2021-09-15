from fastapi import APIRouter, Depends
from starlette import status

from accounting_service.shop.schemas import Shop, BaseShop
from accounting_service.shop.service import ShopService

router = APIRouter(prefix='/shops', tags=['shop'])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=Shop)
def create_shop(shop_create: BaseShop,
                service: ShopService = Depends()):
    shop = service.create_shop(shop_create)
    return shop


@router.patch('/{shop_id}',
              status_code=status.HTTP_202_ACCEPTED,
              response_model=Shop)
def update_shop(shop_id: int,
                shop_update: BaseShop,
                service: ShopService = Depends()):
    shop = service.update_shop(shop_id, shop_update)
    return shop


@router.delete('/{shop_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id: int,
                service: ShopService = Depends()):
    service.delete_shop(shop_id)
    return {}
