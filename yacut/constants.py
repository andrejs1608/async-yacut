import os


DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
UPLOAD_PATH = 'app:/{}'

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
BASE_API_URL = f'{API_HOST}{API_VERSION}/disk/resources'

REQUEST_UPLOAD_URL = f'{BASE_API_URL}/upload'
REQUEST_DOWNLOAD_URL = f'{BASE_API_URL}/download'
API_RESOURCES_URL = BASE_API_URL
PUBLISH_URL = f'{API_RESOURCES_URL}/publish'

UPLOAD_ERROR = 'Ошибка при загрузке файлов на облачное хранилище: {}'
SHORT_NOT_FOUND = 'Указанный id не найден'
NO_BODY = 'Отсутствует тело запроса'
EMPTY_FIELD = '"url" является обязательным полем!'
