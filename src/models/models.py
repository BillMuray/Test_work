from pydantic import BaseModel
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
    quality: Optional[int]
    width: Optional[int]
    high: Optional[int]


class Picture(BaseModel):
    image: Optional[bytes]
    extension: Optional[str]
    size: Optional[str]




