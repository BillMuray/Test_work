import io
from pathlib import Path
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from aiohttp.test_utils import TestClient
from tests.conftest import AUTHORIZATION_HEADER


class TestGetImage:

    TEST_PIC_2 = Path(Path(__file__).parent.parent, 'test_pic2.jpg')

    async def test_success_get_jpeg_image(self, test_client: TestClient):

        with open(self.TEST_PIC_2, 'rb') as test_pic:
            raw_response = await test_client.post(
                path='picture', headers=AUTHORIZATION_HEADER, data=test_pic
            )
            response = await raw_response.json()
        picture_id = response['picture_id']

        query = {'picture_id': picture_id}

        raw_response = await test_client.get(
            path='picture', headers=AUTHORIZATION_HEADER, params=query)

        body_response = await raw_response.read()
        image = Image.open(io.BytesIO(body_response))
        assert raw_response.status == 200
        assert isinstance(image, JpegImageFile)
        assert raw_response.content_type == 'image/jpeg'
