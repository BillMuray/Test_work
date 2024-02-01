from aiohttp import web
from typing import Callable, Any
from utils import get_bearer_token_from_request
from src.models.configurations import config
from loguru import logger
import uuid
from datetime import datetime
import time


async def access_check_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:

        token_from_request = get_bearer_token_from_request(request)

        if config.token == token_from_request:
            return await view(request)
        else:
            return web.Response(text='Доступ заперщен')

    return middleware


async def logger_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:

        with logger.contextualize(
            time=datetime.utcfromtimestamp(time.time()),
            ip=request.remote,
            endpoint=request.path,
            method=request.method,
            request_id=uuid.uuid4().hex[:12],
            params=request.query,
            input_json=request.json()
        ):
            return await view(request)
    return middleware
