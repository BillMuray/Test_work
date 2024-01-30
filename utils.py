from aiohttp import web
from typing import Optional


def get_bearer_token_from_request(request: web.Request) -> Optional[str]:
    token = None
    data = request.headers.get('Authorization')

    if data and data.startswith('Bearer'):
        token = data.split('Bearer')[-1].strip()
    return token


