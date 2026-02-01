import os


DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
BASE_API_URL = f'{API_HOST}{API_VERSION}/disk/resources'

API_RESOURCES_URL = BASE_API_URL
PUBLISH_URL = f'{API_RESOURCES_URL}/publish'
REQUEST_DOWNLOAD_URL = f'{BASE_API_URL}/download'
REQUEST_UPLOAD_URL = f'{BASE_API_URL}/upload'
UPLOAD_PATH = 'app:/{}'

CHOOSE_FILES = 'Выберите хотя бы один файл'
EMPTY_FIELD = '"url" является обязательным полем!'
FIELD_REQUIRED = 'Обязательное поле'
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
LINK_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'
NO_BODY = 'Отсутствует тело запроса'
SHORT_LINK_DESC = 'Короткая ссылка не длиннее 16 символов'
SHORT_NOT_FOUND = 'Указанный id не найден'
UNIQUE_ID_ERROR = 'Не удалось сгенерировать уникальный ID'
UPLOAD_ERROR = 'Ошибка при загрузке файлов на облачное хранилище: {}'

MAX_GENERATE_ATTEMPTS = 10
ORIGINAL_URL_SIZE = 2048
SHORT_ID_LENGTH = 6
SHORT_URL_SIZE = 16
