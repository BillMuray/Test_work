import json
import traceback

from aiohttp import web
from typing import Optional
import auth
from src.models.configurations import LOG_FILE_NAME
from loguru import logger
import sys


def get_bearer_token_from_request(request: web.Request) -> Optional[str]:
    token = None
    data = request.headers.get('Authorization')

    if data and data.startswith('Bearer'):
        token = data.split('Bearer')[-1].strip()
    return token


def log_format(record: dict) -> str:
    dict_log = {
        'level': record['level'].name,
        'time': record['time'].isoformat(),
        'request_id': record['extra'].get('request_id', None),
        'ip': record['extra'].get('ip', None),
        'method': record['extra'].get('method', None),
        'endpoint': record['extra'].get('endpoint', None),
        'params': record['extra'].get('params', None),
        'input_json': record['extra'].get('input_json', None),
        'message': record.get('message', '').replace('\n', ' ')
    }
    if record.get('exception', None):
        dict_log['error'] = traceback.format_exc().replace('\n', ' | ')

    record['extra']['json_log'] = json.dumps(dict_log, ensure_ascii=False)
    return '{extra[json_log]}\n'


def init_logger() -> None:
    logger.remove()
    if auth.ENABLE_LOGS:

        if auth.ENABLE_FILE_LOGS:
            logger.add(
                LOG_FILE_NAME,
                colorize=True,
                level='DEBUG',
                format=log_format,
                backtrace=False,
                diagnose=False,
            )

        if auth.ENABLE_STDOUT_LOGS:
            logger.add(
                sys.stdout,
                colorize=True,
                level='DEBUG',
                format=log_format,
                backtrace=False,
                diagnose=False,
            )
