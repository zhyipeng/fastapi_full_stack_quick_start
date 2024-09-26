__all__ = ['init_db', 'engine', 'async_session', 'Base']

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr
from zhtools.data_structs.convertors import camel_case_to_underline

from .settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr  # type: ignore
    def __tablename__(cls):
        return camel_case_to_underline(cls.__name__)


engine = create_async_engine(settings.DB_URL, echo=settings.DEBUG)


async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()
