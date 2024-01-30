from aiohttp import web
from server import Server
from src.api.middlewares import access_check_middleware


def run() -> None:
    server = Server(
        application=web.Application(middlewares=[access_check_middleware])
    )

    try:
        server.run()
    except Exception as e:
        raise e


if __name__ == "__main__":
    run()
