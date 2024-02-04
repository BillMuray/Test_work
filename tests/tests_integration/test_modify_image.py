from pathlib import Path
from aiohttp.test_utils import TestClient
from tests.conftest import AUTHORIZATION_HEADER


class TestModifyImage:

    TEST_PIC_2 = Path(Path(__file__).parent.parent, 'test_pic2.jpg')

    async def test_success_modify_image(self, test_client: TestClient):

        with open(self.TEST_PIC_2, 'rb') as test_pic:
            raw_response = await test_client.post(
                path='picture', headers=AUTHORIZATION_HEADER, data=test_pic
            )
            response = await raw_response.json()
        picture_id = response['picture_id']

        query = {'picture_id': picture_id, 'quality': 100, 'width': 100, 'high': 100}
        raw_response = await test_client.post(
            path='picture/modify', headers=AUTHORIZATION_HEADER, params=query)

        json_response = await raw_response.json()
        picture_size = f'{query["width"]}x{query["high"]}'

        assert raw_response.status == 200
        assert picture_size == json_response.get('size')

