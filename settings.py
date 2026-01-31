import os


class Config(object):
    QLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        os.getenv('DB', 'sqlite:///db.sqlite3')
    )
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-key-for-dev')
    API_HOST = 'https://cloud-api.yandex.net/'


config = Config()
