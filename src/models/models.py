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


class CompressionParams(BaseModel):
    picture_id: Optional[int]
    quality: Optional[int]
    width: Optional[int]
    high: Optional[int]


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
