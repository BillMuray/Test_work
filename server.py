from aiohttp import web
from src.api import db_api
from src.api import views
from loguru import logger as log
import auth


class Server:

    def __init__(self, application: web.Application) -> None:
        self._app: web.Application = application
        self._db: db_api.Database = db_api.db

    async def _on_startup(self, _app: web.Application) -> None:
        await self._db.run_database()
        await self._db.create_tables()

    async def _on_shutdown(self, _app: web.Application) -> None:
        await self._db.connection_pool.close()

    def _setup_app(self) -> None:
        self._app.add_routes(views.routes)
        self._app.on_startup.append(self._on_startup)
        self._app.on_shutdown.append(self._on_shutdown)

    def _run(self) -> None:
        web.run_app(
            app=self._app,
            host=auth.HOST,
            port=auth.PORT
        )
        log.info('server started')

    def run(self) -> None:
        self._setup_app()
        self._run()

    def create_app(self) -> web.Application:
        self._setup_app()
        return self._app
