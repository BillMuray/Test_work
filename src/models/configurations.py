from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent
LOG_FILE_NAME = Path(PROJECT_PATH, 'logs', 'logs.log')


LOGGER_EXTRAS = {
    'ip': '',
    'endpoint': '',
    'method': '',
    'request_id': '',
    'params': '',
    'input_json': ''
}
