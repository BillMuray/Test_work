from src.models.models import ServerConfig
import yaml


def load_config(filename: str) -> ServerConfig:
    with open(filename) as f:
        config_data = yaml.safe_load(f)['server_config']
    return ServerConfig(**config_data)


config = load_config('config.yml')

LOGGER_EXTRAS = {
    'ip': '',
    'endpoint': '',
    'method': '',
    'request_id': '',
    'params': '',
    'input_json': '',
    'traceback': ''
}
LOGURU_JSON_FORMAT = (
    '{{"<m>time</m>": <g>{time:YYYY-MM-DD HH:mm:ss.SSS}:</g>\n'
    '"<m>level</m>": <lvl>{level}</lvl>\n'
    '"<m>request_id</m>": {extra[request_id]}\n'
    '"<m>ip</m>": {extra[ip]}\n'
    '"<m>method</m>": {extra[method]}\n'
    '"<m>endpoint</m>": {extra[endpoint]}\n'
    '"<m>params</m>": {extra[params]}\n'
    '"<m>input_json</m>": {extra[input_json]}\n'
    '"<m>message</m>": <light-blue>{message}</light-blue>}}\n'
)