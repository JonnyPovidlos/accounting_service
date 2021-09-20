from fastapi import Depends
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError, NoResultFound

from accounting_service.account.models import Account as AccountORM
from accounting_service.account.schemas import CreateAccount, LoginAccount
from accounting_service.database import Session, get_session
from exceptions import IdentityError


class AccountService:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password, hash_password) -> bool:
        return pbkdf2_sha256.verify(password, hash_password)

    def create_account(self, account_create: CreateAccount) -> AccountORM:
        account_create.password = self.hash_password(account_create.password)
        account = AccountORM(**account_create.dict(exclude_unset=True))
        self.session.add(account)

        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise IdentityError

    def _get_account(self, limits: dict) -> AccountORM:
        attr = list(limits.keys())[0]
        value = list(limits.values())[0]
        try:
            account = self.session.query(AccountORM).where(AccountORM.__dict__[attr] == value).one()
            return account
        except NoResultFound:
            raise IdentityError

    def login(self, login_account: LoginAccount) -> AccountORM:
        account = self._get_account({'username': login_account.username})
        if self.verify_password(login_account.password, account.password):
            return account
        else:
            raise IdentityError
