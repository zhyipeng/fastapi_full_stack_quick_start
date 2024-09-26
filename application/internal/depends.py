import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from pydantic import BaseModel
from starlette import status

from application.common.db import async_session
from application.common.settings import settings


async def get_db():
    async with async_session() as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


class TokenData(BaseModel):
    username: str


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        logger.info('token expired')
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail='token expired',
        )

    except Exception as e:
        logger.exception(f'jwt unknown error: {e}')
        raise credentials_exception

    # TODO: check user is enabled
    return token_data
