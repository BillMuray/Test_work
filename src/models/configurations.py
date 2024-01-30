from src.models.models import ServerConfig
import yaml


def load_config(filename: str) -> ServerConfig:
    with open(filename) as f:
        config_data = yaml.safe_load(f)['server_config']
    return ServerConfig(**config_data)


config = load_config('config.yml')

