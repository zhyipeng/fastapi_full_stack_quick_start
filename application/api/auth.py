import datetime

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.settings import settings
from application.internal.auth import create_access_token
from application.internal.depends import get_db

router = APIRouter()


class LoginRsp(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
) -> LoginRsp:
    # TODO: check username and password

    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={'sub': form_data.username},
        expires_delta=access_token_expires,
    )
    refresh_token = create_access_token(
        data={'id': form_data.username},
        expires_delta=datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return LoginRsp(
        access_token=access_token, refresh_token=refresh_token, token_type='bearer'
    )


class RefreshReq(BaseModel):
    refresh_token: str


class RefreshRsp(BaseModel):
    access_token: str


@router.post('/refresh')
async def refresh(
    req: RefreshReq,
    session: AsyncSession = Depends(get_db),
) -> RefreshRsp:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            req.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        uid: str = payload.get('id')
        if uid is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        logger.info('token expired')
        raise credentials_exception
    except Exception as e:
        logger.exception(f'jwt error: {e}')
        raise credentials_exception

    # TODO: check user

    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={'sub': 'username'},
        expires_delta=access_token_expires,
    )
    return RefreshRsp(access_token=access_token)
