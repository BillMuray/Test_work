from pathlib import Path

from aiohttp.test_utils import TestClient

from tests.conftest import AUTHORIZATION_HEADER


class TestUploadImage:

    TEST_PIC_2 = Path(Path(__file__).parent.parent, 'test_pic2.jpg')

    async def test_route_without_token(self, test_client: TestClient):
        raw_response = await test_client.post(path='picture')
        text = await raw_response.text()
        assert raw_response.status == 401
        assert text == 'Доступ заперщен'

    async def test_success_upload_jpeg_image(self, test_client: TestClient):
        query = {'quality': 100, 'width': 200, 'high': 200}

        with open(self.TEST_PIC_2, 'rb') as test_pic:
            raw_response = await test_client.post(
                path='picture', headers=AUTHORIZATION_HEADER, params=query, data=test_pic
            )
        response = await raw_response.json()
        assert raw_response.status == 200
        assert response.get('message', '') == 'Изображение добавлено в БД'
