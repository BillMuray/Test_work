import json
from pathlib import Path
from typing import Optional, List
from loguru import logger as log
from aiohttp import web
from src.api import routes as r
from src.api.db_api import db
from src.models.configurations import LOG_FILE_NAME, PROJECT_PATH
from src.models.models import Picture, CompressionParams, LoadPicturesParams
from src.api.pillow_manager import PillowManager as pm
import auth
import csv

routes = web.RouteTableDef()


@routes.post(r.PICTURE)
async def upload_picture(request: web.Request) -> web.Response:

    request_data = await request.read()
    compression_params = CompressionParams(**request.query)

    try:
        picture: Picture = pm.prepare_image_from_binary(
            binary_data=request_data,
            compress=compression_params
        )
        picture_id = await db.add_picture_to_db(picture)
        log.info(f"Изображение добавлено в БД под номером {picture_id}")

    except Exception as e:
        log.warning(f'Не удалось загрузить картинку')
        return web.Response(text=f'Не удалось загрузить картинку: {e}', status=500)

    return web.Response(text=f"Изображение добавлено в БД под номером {picture_id}")


@routes.post(r.MODIFY_PICTURE)
async def modify_picture(request: web.Request) -> web.Response:

    compression_params = CompressionParams(**request.query)

    if compression_params.picture_id is None:
        text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
                        'либо через параметры запроса.'
        log.info(text_response)
        return web.Response(text=text_response, status=400)

    picture = await db.get_picture_from_db(compression_params.picture_id)

    try:
        new_picture = pm.compress_image(picture.image, compression_params)
    except Exception as e:
        return web.Response(text=f'Не удалось произвести компрессию: {e}', status=500)

    new_picture.id = compression_params.picture_id
    await db.replace_picture(new_picture)
    text_response = f"Изображение под номером {new_picture.id} изменено"
    log.info(text_response)
    return web.Response(text=text_response)


@routes.get(r.PICTURE)
async def get_picture(request: web.Request) -> web.Response:

    picture_id: int = await get_picture_id_from_request(request)

    if picture_id is None:
        text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
                        'либо через параметры запроса.'
        log.info(text_response)
        return web.Response(text=text_response, status=400)

    try:
        picture = await db.get_picture_from_db(picture_id)
        log.info(f'Картинка (id={picture_id}) получена из базы данных и передана клиенту')
        return web.Response(body=picture.image, content_type='image/jpeg')
    except Exception as e:
        text_response = f'Такой картинки нет в базе данных. {e}'
        return web.Response(text=text_response, status=404)


@routes.get(r.PICTURE_PARAMETERS)
async def get_picture_parameters(request: web.Request) -> web.Response:

    picture_id: int = await get_picture_id_from_request(request)

    if picture_id is None:
        text_response = 'Не передан параметр "picture_id". Передайте ключ через json, ' \
                        'либо через параметры запроса.'
        log.info(text_response)
        return web.Response(text=text_response, status=400)

    try:
        picture = await db.get_picture_from_db(picture_id)
        log.info(f'Параметры картинки (id={picture_id}) '
                 f'получены из базы данных и переданы клиенту')
        return web.Response(body=json.dumps(picture.dict(exclude={"image"})))

    except Exception as e:
        text_response = f'Такой картинки нет в базе данных. {e}'
        return web.Response(text=text_response, status=404)


@routes.get(r.PICTURES_PARAMETERS)
async def load_pictures_parameters(request: web.Request) -> web.StreamResponse:
    params = LoadPicturesParams(**request.query)

    dump = await db.get_all_pictures()

    if params.dump_format == 'csv':
        return web.FileResponse(path=write_csv(dump))
    else:
        return web.Response(body=write_json(dump))


@routes.get(r.LOGS)
async def load_logs(_request: web.Request) -> web.Response:

    if auth.ENABLE_LOGS and auth.ENABLE_FILE_LOGS:
        with open(LOG_FILE_NAME) as file:
            return web.json_response(text=file.read(), status=200)
    else:
        return web.json_response(text='Логирование в файл отключено', status=200)


def write_json(dump: List[Picture]) -> str:
    images = [pic.dict(exclude={'image'}) for pic in dump]
    json_data: str = json.dumps({'images': images}, indent=3)
    log.info('json успешно сформирован')
    return json_data


def write_csv(dump: List[Picture]) -> Path:
    filepath = Path(PROJECT_PATH, 'dumps.csv')
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['picture_id', 'format', 'size'])
        for picture in dump:
            writer.writerow(picture.dict(exclude={'image'}).values())

    log.info('csv успешно сформирован')
    return filepath


async def get_picture_id_from_request(request: web.Request) -> Optional[int]:

    picture_id: str = request.query.get('picture_id')
    if picture_id is None:
        json_request: dict = {}
        try:
            json_request: dict = await request.json()
        finally:
            picture_id = json_request.get('picture_id')
    return int(picture_id)
