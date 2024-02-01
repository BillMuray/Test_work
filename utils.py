from aiohttp import web
from typing import Optional
from src.models.configurations import LOGURU_JSON_FORMAT
from loguru import logger
import sys


def get_bearer_token_from_request(request: web.Request) -> Optional[str]:
    token = None
    data = request.headers.get('Authorization')

    if data and data.startswith('Bearer'):
        token = data.split('Bearer')[-1].strip()
    return token


def init_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        level='DEBUG',
        format=LOGURU_JSON_FORMAT,
        backtrace=False,
        diagnose=False,
    )
    logger.opt(exception=False)
