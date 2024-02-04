import asyncio

import pytest

import auth
import tests.test_auth
from server import Server
from aiohttp import web
from aiohttp.test_utils import TestServer, TestClient

from src.api.middlewares import access_check_middleware


AUTHORIZATION_HEADER = {'Authorization': f'Bearer {tests.test_auth.TOKEN}'}


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def test_client():
    auth.TOKEN = tests.test_auth.TOKEN
    auth.POSTGRES_HOST = tests.test_auth.POSTGRES_HOST
    auth.POSTGRES_PORT = tests.test_auth.POSTGRES_PORT
    auth.POSTGRES_USER = tests.test_auth.POSTGRES_USER
    auth.POSTGRES_DB = tests.test_auth.POSTGRES_DB
    auth.POSTGRES_PASSWORD = tests.test_auth.POSTGRES_PASSWORD

    server = Server(
        application=web.Application(middlewares=[access_check_middleware])
    )
    app = server.create_app()

    server = TestServer(app)
    client = TestClient(server)

    await client.start_server()
    yield client
    await client.close()
