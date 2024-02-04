import json

from aiohttp import web
from typing import Callable, Any

from pydantic.error_wrappers import ValidationError

from utils import get_bearer_token_from_request
from loguru import logger
import uuid
import auth


async def access_check_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:

        token_from_request = get_bearer_token_from_request(request)

        if auth.TOKEN != token_from_request:
            return web.Response(text='Доступ заперщен', status=401)
        try:
            result = await view(request)

        except ValidationError:
            logger.info(f'Ошибка валидации')
            return web.Response(text='Ошибка валидации', status=401)

        except Exception:
            logger.info(f'Неопознанная ошибка')
            return web.Response(text='Неопознанная ошибка', status=500)

        return result

    return middleware


async def logger_middleware(_app: web.Application, view: Callable) -> Callable:
    async def middleware(request: web.Request) -> Any:

        with logger.contextualize(
            ip=request.remote,
            endpoint=request.path,
            method=request.method,
            request_id=uuid.uuid4().hex[:12],
            params=json.dumps(dict(request.query), ensure_ascii=False)
        ):
            return await view(request)
    return middleware
