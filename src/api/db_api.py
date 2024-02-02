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
            image bytea,
            format VARCHAR(255),
            size VARCHAR(255)
            )
            """
        async with self.connection_pool.acquire() as connection:
            await connection.execute(request)

    async def add_picture_to_db(self, picture: Picture) -> str:

        request = """INSERT INTO pictures(image, format, size) 
                     VALUES($1,$2,$3) RETURNING ID"""
        return await self.connection_pool.fetchval(
            request, picture.image, picture.format, picture.size)

    async def get_picture_from_db(self, picture_id: int) -> bytes:
        request = f"SELECT image FROM pictures WHERE id=$1"
        return await self.connection_pool.fetchval(
            request, picture_id)

    async def get_picture_params_from_db(self, picture_id: int) -> dict:

        request = f"SELECT id, format, size FROM pictures WHERE id=$1"
        response = await self.connection_pool.fetchrow(request, picture_id)
        picture = Picture(**response)
        return picture.dict(exclude={"image"})


db = Database()


