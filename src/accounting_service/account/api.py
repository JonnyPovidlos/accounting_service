from fastapi import (APIRouter,
                     Depends,
                     status,
                     HTTPException)
from fastapi.security import OAuth2PasswordRequestForm

from accounting_service.account.schemas import CreateAccount, Account, LoginAccount
from accounting_service.account.service import AccountService
from accounting_service.auth import Token, create_token
from exceptions import IdentityError

router = APIRouter(prefix='/accounts', tags=['account'])


@router.post('/sign-up',
             response_model=Token,
             status_code=status.HTTP_201_CREATED)
def create_account(
        account_create: CreateAccount,
        service: AccountService = Depends()
):
    try:
        account = service.create_account(account_create)
        return Token(
            access_token=create_token(account),
            token_type='bearer'
        )
    except IdentityError:
        raise HTTPException(status.HTTP_409_CONFLICT)


@router.post('/sign-in',
             response_model=Token)
def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        service: AccountService = Depends()
):
    try:
        account_login = LoginAccount(username=credentials.username,
                                     password=credentials.password)
        account = service.login(account_login)
        token = Token(
            access_token=create_token(account),
            token_type='bearer'
        )
        return token
    except IdentityError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
