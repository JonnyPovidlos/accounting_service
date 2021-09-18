from fastapi import (APIRouter,
                     Depends,
                     status,
                     HTTPException)

from accounting_service.account.schemas import CreateAccount, Account
from accounting_service.account.service import AccountService
from exceptions import IdentityError

router = APIRouter(prefix='/accounts', tags=['account'])


@router.post('',
             response_model=Account,
             status_code=status.HTTP_201_CREATED)
def create_account(
        account_create: CreateAccount,
        service: AccountService = Depends()
):
    try:
        account = service.create_account(account_create)
        return account
    except IdentityError:
        raise HTTPException(status.HTTP_409_CONFLICT)

