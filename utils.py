import json
import csv
import traceback
from pathlib import Path
from aiohttp import web
from typing import Optional, List
import auth
from src.models.configurations import LOG_FILE_NAME, PROJECT_PATH
from loguru import logger as log
from src.models.models import Picture
import sys


def get_bearer_token_from_request(request: web.Request) -> Optional[str]:
    token = None
    data = request.headers.get('Authorization')

    if data and data.startswith('Bearer'):
        token = data.split('Bearer')[-1].strip()
    return token


def write_json(dump: List[Picture]) -> str:
    images = [pic.dict(exclude={'image'}) for pic in dump]
    json_data: str = json.dumps({'images': images}, indent=3)
    log.info('json успешно сформирован')
    return json_data


def write_csv(dump: List[Picture]) -> Path:
    filepath = Path(PROJECT_PATH, 'dumps.csv')
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['picture_id', 'format', 'size'])
        for picture in dump:
            writer.writerow(picture.dict(exclude={'image'}).values())

    log.info('csv успешно сформирован')
    return filepath


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
        'message': record.get('message', '').replace('\n', ' '),
        'traceback': traceback.format_exc().replace('NoneType: None\n', 'None').replace('\n', ' | ')
    }
    record['extra']['json_log'] = json.dumps(dict_log, ensure_ascii=False)
    return '{extra[json_log]}\n'


def init_logger() -> None:
    log.remove()
    if auth.ENABLE_LOGS:

        if auth.ENABLE_FILE_LOGS:
            log.add(
                LOG_FILE_NAME,
                colorize=True,
                level='DEBUG',
                format=log_format,
                backtrace=False,
                diagnose=False,
            )
            log.opt(exception=False)
        if auth.ENABLE_STDOUT_LOGS:
            log.add(
                sys.stdout,
                colorize=True,
                level='DEBUG',
                format=log_format,
                backtrace=False,
                diagnose=False,
            )
            log.opt(exception=False)
