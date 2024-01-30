from aiohttp import web
from typing import Callable, Any
from utils import get_bearer_token_from_request
from src.models.configurations import config


async def access_check_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:

        token_from_request = get_bearer_token_from_request(request)

        if config.token == token_from_request:
            return await view(request)
        else:
            return web.Response(text='Доступ заперщен')

    return middleware
