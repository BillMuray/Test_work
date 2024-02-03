import json

from aiohttp import web
from typing import Callable, Any
from utils import get_bearer_token_from_request
from loguru import logger
import uuid
import auth


async def access_check_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:

        token_from_request = get_bearer_token_from_request(request)

        if auth.TOKEN != token_from_request:
            return web.Response(text='Доступ заперщен')

        return await view(request)

    return middleware


async def logger_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:
        with logger.contextualize(
            ip=request.remote,
            endpoint=request.path,
            method=request.method,
            request_id=uuid.uuid4().hex[:12],
            params=json.dumps(dict(request.query), ensure_ascii=False),
            input_json=await request.json() if request.body_exists else None
        ):
            return await view(request)
    return middleware
