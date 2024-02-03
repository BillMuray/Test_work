from typing import Optional, List
import asyncpg
import auth
from src.models.models import Picture


class Database:

    def __init__(self) -> None:
        self.connection_pool: Optional[asyncpg.Pool] = None

    async def run_database(self) -> None:
        self.connection_pool = await asyncpg.create_pool(
            database=auth.POSTGRES_DB,
            user=auth.POSTGRES_USER,
            password=auth.POSTGRES_PASSWORD,
            host=auth.POSTGRES_HOST,
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
        request = """INSERT INTO pictures (image, format, size) 
                     VALUES($1,$2,$3) RETURNING ID"""
        return await self.connection_pool.fetchval(
            request, picture.image, picture.format, picture.size)

    async def get_picture_from_db(self, picture_id: int) -> Picture:
        request = f"SELECT * FROM pictures WHERE id=$1"
        response = await self.connection_pool.fetchrow(request, picture_id)
        picture = Picture(**response)
        return picture

    async def replace_picture(self, picture: Picture):
        request = """UPDATE pictures SET (image, format, size) = ($2,$3,$4) WHERE id = $1"""
        return await self.connection_pool.execute(
            request, picture.id, picture.image, picture.format, picture.size)

    async def get_all_pictures(self) -> List[Picture]:
        response = await self.connection_pool.fetch(f"SELECT id, format, size FROM pictures ORDER BY id asc")
        return [Picture(**raw_pic) for raw_pic in response]


db = Database()
