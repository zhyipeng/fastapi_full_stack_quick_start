from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from application.api import api_router
from application.common.db import init_db
from application.common.exceptions import BusinessException
from application.common.log import init_logger
from application.common.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting up')
    init_logger()
    async with init_db():
        yield


app = FastAPI(lifespan=lifespan, debug=settings.DEBUG)
app.include_router(api_router, prefix='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(BusinessException)
async def handle_business_exception(request, exc: BusinessException):
    return JSONResponse(
        {
            'code': exc.error_code,
            'error_message': exc.error_message,
        }
    )


app.mount('/assets', StaticFiles(directory='frontend/dist/assets'), name='assets')


@lru_cache
def get_index_html():
    return HTMLResponse(Path('frontend/dist/index.html').read_text())


@app.get('/')
def index():
    return get_index_html()
