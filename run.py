from aiohttp import web
from server import Server
from src.api.middlewares import logger_middleware, access_check_middleware
from loguru import logger as log
from utils import init_logger
from src.models.configurations import LOGGER_EXTRAS


def run() -> None:
    server = Server(
        application=web.Application(
            middlewares=[logger_middleware, access_check_middleware]
        )
    )

    try:
        server.run()
    except Exception as e:
        raise e


if __name__ == "__main__":

    init_logger()

    with log.contextualize(**LOGGER_EXTRAS):
        run()
