from fastapi import Depends
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from accounting_service.account.models import Account as AccountORM
from accounting_service.account.schemas import CreateAccount
from accounting_service.database import Session, get_session
from exceptions import IdentityError


class AccountService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_account(self, account_create: CreateAccount):
        account_create.password = pbkdf2_sha256.hash(account_create.password)
        account = AccountORM(**account_create.dict(exclude_unset=True))
        self.session.add(account)

        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise IdentityError
