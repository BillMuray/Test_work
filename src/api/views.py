import json
from loguru import logger as log
from aiohttp import web
from src.api import routes as r
from src.api.db_api import db
from src.models.configurations import LOG_FILE_NAME
from src.models.models import Picture, CompressionParams, LoadPicturesParams, ModifyCompressionParams, PictureGetParams
from src.api.pillow_manager import PillowManager as pm
from utils import write_csv, write_json
import auth

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

    return web.json_response(data={'picture_id': picture_id, 'message': "Изображение добавлено в БД"})


@routes.post(r.MODIFY_PICTURE)
async def modify_picture(request: web.Request) -> web.Response:
    compression_params = ModifyCompressionParams(**request.query)

    picture = await db.get_picture_from_db(compression_params.picture_id)

    try:
        new_picture = pm.compress_image(picture.image, compression_params)
    except Exception as e:
        log.warning('Не удалось произвести компрессию')
        return web.Response(text=f'Не удалось произвести компрессию: {e}', status=500)

    new_picture.id = compression_params.picture_id
    await db.replace_picture(new_picture)
    log.info(f"Изображение под номером {new_picture.id} изменено")
    return web.json_response(data={'picture_id': new_picture.id,
                                   'size': new_picture.size,
                                   'format': new_picture.format,
                                   'message': "Изображение успешно изменено"
                                   })


@routes.get(r.PICTURE)
async def get_picture(request: web.Request) -> web.Response:
    picture_id = PictureGetParams(**request.query).picture_id

    try:
        picture = await db.get_picture_from_db(picture_id)
        log.info(f'Картинка (id={picture_id}) получена из базы данных и передана клиенту')
        return web.Response(body=picture.image, content_type='image/jpeg')
    except Exception as e:
        log.warning('Не удалось получить картинку')
        return web.Response(text=f'Такой картинки нет в базе данных. {e}', status=404)


@routes.get(r.PICTURE_PARAMETERS)
async def get_picture_parameters(request: web.Request) -> web.Response:
    picture_id = PictureGetParams(**request.query).picture_id
    try:
        picture = await db.get_picture_from_db(picture_id)
        log.info(f'Параметры картинки (id={picture_id}) '
                 f'получены из базы данных')
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
async def load_logs(_request: web.Request) -> web.StreamResponse:

    if auth.ENABLE_LOGS and auth.ENABLE_FILE_LOGS:
        return web.FileResponse(path=LOG_FILE_NAME, status=200)
    else:
        return web.json_response(text='Логирование в файл отключено', status=200)
