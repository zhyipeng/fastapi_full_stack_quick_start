from fastapi import APIRouter

from . import auth

api_router = APIRouter()

for module in [auth]:
    name = module.__name__.split('.')[-1]
    api_router.include_router(module.router, prefix=f'/{name}', tags=[name])
