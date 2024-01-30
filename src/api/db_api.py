from typing import Optional
import asyncpg
from src.models.configurations import config
from src.models.models import Picture


class Database:

    def __init__(self) -> None:
        self.connection_pool: Optional[asyncpg.Pool] = None

    async def run_database(self) -> None:
        self.connection_pool = await asyncpg.create_pool(
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            host=config.POSTGRES_HOST,
        )
        print('Database has been successfully initialized ')

    async def create_tables(self) -> None:
        request = """
            CREATE TABLE IF NOT EXISTS pictures(
            ID SERIAL PRIMARY KEY,
            image bytea)
            """
        async with self.connection_pool.acquire() as connection:
            await connection.execute(request)

    async def add_image(self, image: object) -> str:
        request = """INSERT INTO pictures(image) VALUES($1) RETURNING ID"""
        return await self.connection_pool.fetchval(request, image)



db = Database()


