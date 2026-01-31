import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB')
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_HOST = 'https://cloud-api.yandex.net/'


config = Config()
