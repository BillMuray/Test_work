from aiohttp import web
from src.api import db_api
from src.api import views
from src.models.configurations import config


class Server:

    def __init__(self, application: web.Application) -> None:
        self._app: web.Application = application
        self._db: db_api.Database = db_api.db

    async def _on_startup(self, _app: web.Application) -> None:
        await self._db.run_database()
        await self._db.create_tables()

    async def _on_shutdown(self, _app: web.Application) -> None:
        await self._db.connection_pool.close()

    def _run(self) -> None:
        web.run_app(
            app=self._app,
            host=config.host,
            port=config.port
        )

    def run(self) -> None:
        print("start server")
        self._app.add_routes(views.routes)
        self._app.on_startup.append(self._on_startup)
        self._app.on_shutdown.append(self._on_shutdown)

        self._run()
