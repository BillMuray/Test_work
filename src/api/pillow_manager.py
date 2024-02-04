import io
from PIL import Image
from src.models.models import Picture, CompressionParams
from typing import Optional, Union


class PillowManager:
    @classmethod
    def prepare_image_from_binary(cls, binary_data: bytes,
                                  compress: Optional[CompressionParams]) -> Optional[Picture]:

        picture: Picture = Picture()
        try:
            image = Image.open(io.BytesIO(binary_data))
        except Exception as e:
            raise e

        if compress or image.format != 'JPEG':
            image = image.convert('RGB')
            try:

                picture = cls.compress_image(image=image, compression_params=compress)
            except Exception as e:
                raise e
        else:
            picture.image = binary_data
            picture.size = str(image.size[0]) + 'x' + str(image.size[1])
            picture.format = image.format

        return picture

    @classmethod
    def compress_image(cls, image: Union[Image.Image, bytes], compression_params: CompressionParams):

        if compression_params.width is None:
            compression_params.width = image.size[0]
        if compression_params.high is None:
            compression_params.high = image.size[1]

        picture: Picture = Picture()

        if type(image) is bytes:
            image = Image.open(io.BytesIO(image))
        compressed_image = image.resize(size=(compression_params.width,
                                              compression_params.high)
                                        )

        picture.image = cls.image_to_byte_array(image=compressed_image,
                                                quality=compression_params.quality)
        picture.size = str(compressed_image.size[0]) + 'x' + str(compressed_image.size[1])
        picture.format = 'JPEG'
        return picture

    @classmethod
    def image_to_byte_array(cls, image: Image, quality: Optional[int]):

        if quality is None:
            quality = 100

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality)
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
