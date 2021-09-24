from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

from config import Config


class Token(BaseModel):
    access_token: str
    token_type: str


oauth_schema = OAuth2PasswordBearer('/accounts/sign-in')


def create_token(account: 'Account') -> str:
    now = datetime.utcnow()
    return jwt.encode(
        {
            'sub': str(account.id),
            'exp': now + timedelta(seconds=300),
            'iat': now,
            'nbf': now,
            'account': {
                'id': account.id,
                'username': account.username,
                'email': account.email
            }
        },
        Config.SECRET_KEY,
        'HS256'
    )


def get_current_account(
        token: str = Depends(oauth_schema)
) -> 'Account':
    from accounting_service.account.schemas import Account
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Error',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    token_data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    if 'account' not in token_data:
        raise credential_exception
    return Account(**token_data['account'])
