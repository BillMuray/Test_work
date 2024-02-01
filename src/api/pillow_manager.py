import io
from PIL import Image
from src.models.models import Picture, CompressionParams
from typing import Optional


class PillowManager:
    @classmethod
    def prepare_image_from_binary(cls, binary_data: bytes,
                                  compress: Optional[CompressionParams]) -> Picture:

        picture: Picture = Picture()
        image = Image.open(io.BytesIO(binary_data))
        if compress:
            binary_data = cls.compress_image(image=image, compression_params=compress)

        picture.image = binary_data
        picture.size = str(image.size[0]) + 'x' + str(image.size[1])
        picture.format = image.format

        return picture

    @classmethod
    def compress_image(cls, image: Image, compression_params: CompressionParams):

        if compression_params.width is None:
            compression_params.width = image.size[0]
        if compression_params.high is None:
            compression_params.high = image.size[1]

        compressed_image = image.resize(size=(compression_params.width,
                                              compression_params.high)
                                        )
        return cls.image_to_byte_array(image=compressed_image,
                                       quality=compression_params.quality)

    @classmethod
    def image_to_byte_array(cls, image: Image, quality: Optional[int]):

        if quality is None:
            quality = 100

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=quality)
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

