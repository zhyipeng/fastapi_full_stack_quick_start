__all__ = ['settings']

import os.path

from loguru import logger
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    ENV: str = 'test'
    DB_URL: str = 'sqlite+aiosqlite:///data.db?charset=utf8mb4'
    # use "openssl rand -hex 32' to gen secret key
    SECRET_KEY: str = 'b0e177c27aed7482f30330337a06784bc22e6dbf8ae19bcada19484da2c09928'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 4 * 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    LOGPATH: str = 'log'

    class Config:
        env_file = '.env'


settings = Settings()

logger.add(os.path.join(settings.LOGPATH, 'app.log'))
