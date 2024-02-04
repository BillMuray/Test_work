from pydantic import BaseModel, validator, ValidationError
from typing import Optional


class ServerConfig(BaseModel):
    host: str
    port: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    token: str


class PictureGetParams(BaseModel):
    picture_id: int


class CompressionParams(BaseModel):
    quality: Optional[int]
    width: Optional[int]
    high: Optional[int]

    @validator('quality')
    def check_quality(cls, value: Optional[int]) -> Optional[int]:
        if value:
            if 0 < value > 100:
                raise ValidationError(f'Параметр ''quality'' может быть от 0 до 100')
        return value


class ModifyCompressionParams(CompressionParams):
    picture_id: int


class Picture(BaseModel):
    id: Optional[int]
    image: Optional[bytes]
    format: Optional[str]
    size: Optional[str]


class LoadPicturesParams(BaseModel):
    dump_format: str

    @validator('dump_format')
    def check_format(cls, value: str) -> str:
        if value.lower() not in ('csv', 'json'):
            raise ValidationError(f'Не верный формат (только csv или json)')

        return value.lower()
