import json
from typing import Optional
from loguru import logger as log
from aiohttp import web
from src.api import routes as r
from src.api.db_api import db
from src.models.models import Picture, CompressionParams
from src.api.pillow_manager import PillowManager as pm

routes = web.RouteTableDef()


@routes.post(r.PUT_PICTURE)
async def put_picture(request: web.Request) -> web.Response:

    picture = Picture()
    text_response: str = ''

    request_data = await request.read()
    compression_params = CompressionParams(**request.query)

    try:
        picture = pm.prepare_image_from_binary(
            binary_data=request_data,
            compress=compression_params
        )

    except Exception as e:
        log.warning(f'Не удалось загрузить картинку')
        text_response = f'Не удалось загрузить картинку: {e}'
        return web.Response(text=text_response)

    if picture.image:
        picture_id = await db.add_picture_to_db(picture)
        text_response = f"Изображение добавлено в БД под номером {picture_id}"
        log.info(f'Изображение добавлено в БД под номером {picture_id}')

    return web.Response(text=text_response)


@routes.post(r.MODIFY_PICTURE)
async def get_picture(request: web.Request) -> web.Response:

    compression_params = CompressionParams(**request.query)

    if compression_params.picture_id is None:
        text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
                        'либо через параметры запроса.'
        log.info(text_response)
        return web.Response(text=text_response)

    pass


@routes.get(r.GET_PICTURE)
async def get_picture(request: web.Request) -> web.Response:

    picture_id: int = await get_picture_id_from_request(request)

    if picture_id is None:
        text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
                        'либо через параметры запроса.'
        log.info(text_response)
        return web.Response(text=text_response)

    try:
        image: bytes = await db.get_picture_from_db(picture_id)
        log.info(f'Картинка (id={picture_id}) получена из базы данных и передана клиенту')
        return web.Response(body=image, content_type='application/octet-stream')
    except Exception as e:
        text_response = f'Такой картинки нет в базе данных. {e}'
        return web.Response(text=text_response)


@routes.get(r.GET_PICTURE_PARAMETERS)
async def get_picture_parameters(request: web.Request) -> web.Response:

    picture_id: int = await get_picture_id_from_request(request)

    if picture_id is None:
        text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
                        'либо через параметры запроса.'
        log.info(text_response)
        return web.Response(text=text_response)

    try:
        params = await db.get_picture_params_from_db(picture_id)
        log.info(f'Параметры картинки (id={picture_id}) '
                 f'получены из базы данных и переданы клиенту')
        return web.Response(body=json.dumps(params))

    except Exception as e:
        text_response = f'Такой картинки нет в базе данных. {e}'
        return web.Response(text=text_response)


async def get_picture_id_from_request(request: web.Request) -> Optional[int]:

    picture_id: str = request.query.get('picture_id')
    if picture_id is None:
        json_request: dict = {}
        try:
            json_request: dict = await request.json()
        finally:
            picture_id = json_request.get('picture_id')
    return int(picture_id)


# async def check_picture_id(view):
#     async def middleware(request: web.Request):
#         picture_id = request.query.get('picture_id')
#         if picture_id is None:
#             text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
#                             'либо через параметры запроса.'
#             log.info(text_response)
#             return web.Response(text=text_response)
#
#         return await view(request)
#
#     return middleware