import io

from aiohttp import web
from src.api import routes as r
from src.api.db_api import db
from src.models.models import Picture, CompressionParams
from PIL import Image

routes = web.RouteTableDef()


@routes.post(r.PUT_PICTURE)
async def put_picture(request: web.Request) -> web.Response:


    request_data = await request.read()

    compression_params = CompressionParams(**request.query)

    image = Image.open(io.BytesIO(request_data))

    picture_id = await db.add_image(request_data)

    return web.Response(text=f"Изображение добавлено в БД под номером {picture_id}")






