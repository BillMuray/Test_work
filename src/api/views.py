
from loguru import logger as log
from aiohttp import web
from src.api import routes as r
from src.api.db_api import db
from src.models.models import Picture, CompressionParams
from src.api.pillow_manager import PillowManager as pm

routes = web.RouteTableDef()


@routes.post(r.PUT_PICTURE)
async def put_picture(request: web.Request) -> web.Response:

    picture: Picture = Picture()
    text_response = ''

    request_data = await request.read()
    compression_params = CompressionParams(**request.query)

    try:
        picture = pm.prepare_image_from_binary(
            binary_data=request_data,
            compress=compression_params
        )

    except Exception:
        log.warning(f'Не удалось загрузить картинку')
        text_response = 'Не удалось загрузить картинку'

    if picture.image:
        picture_id = await db.add_image(picture)
        text_response = f"Изображение добавлено в БД под номером {picture_id}"
        log.info(f'Изображение добавлено в БД под номером {picture_id}')

    return web.Response(text=text_response)






