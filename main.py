import os

import uvicorn
from typer import Typer

from application import app

cli = Typer(no_args_is_help=True)


@cli.command()
def init():
    """初始化项目"""
    os.system('cd frontend && pnpm install && pnpm run build')


@cli.command()
def dev(host: str = '0.0.0.0', port: int = 8000):
    """启动开发服务"""
    os.system(f'uvicorn application:app --reload --host {host} --port {port}')


@cli.command()
def build_frontend():
    """构建前端"""
    os.system('cd frontend && pnpm run build')


@cli.command()
def genapi():
    """更新/生成前端sdk"""
    os.system('cd frontend && pnpm run gen')


@cli.command()
def lock_requirements():
    """更新/生成requirements.txt"""
    os.system('uv pip freeze | uv pip compile - -o requirements.txt ')


@cli.command()
def run(host: str = '0.0.0.0', port: int = 8000):
    """启动服务"""
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    cli()
