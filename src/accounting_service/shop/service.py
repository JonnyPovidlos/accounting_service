from fastapi import Depends
from sqlalchemy.exc import NoResultFound

from accounting_service.database import get_session, Session, update_attrs
from accounting_service.shop.models import Shop as ShopORM
from accounting_service.shop.schemas import BaseShop
from exceptions import NoResultFoundCustom


class ShopService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_shop(self, shop_create: BaseShop, account_id) -> ShopORM:
        shop = ShopORM(**shop_create.dict(exclude_unset=True), account_id=account_id)
        self.session.add(shop)
        self.session.commit()
        return shop

    def _get(self, shop_id: int, account_id) -> ShopORM:
        try:
            shop = self.session.query(ShopORM).filter(ShopORM.id == shop_id
                                                      and ShopORM.account_id == account_id).one()
            return shop
        except NoResultFound:
            raise NoResultFoundCustom

    def update_shop(self, shop_id: int, shop_update: BaseShop, account_id) -> ShopORM:
        shop = self._get(shop_id, account_id)
        update_attrs(shop, shop_update)
        self.session.commit()
        return shop

    def delete_shop(self, shop_id, account_id):
        shop = self._get(shop_id, account_id)
        self.session.delete(shop)
        self.session.commit()

