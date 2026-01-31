import re
import random
import string
from datetime import datetime
from flask import url_for
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    class ObjectCreateError(Exception):
        pass

    class ShortGenerateError(Exception):
        pass

    @staticmethod
    def get_unique_short_id():
        chars = string.ascii_letters + string.digits
        for _ in range(10):
            short_id = ''.join(random.choices(chars, k=6))
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id
        raise URLMap.ShortGenerateError(
            'Не удалось сгенерировать уникальный ID'
        )

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @classmethod
    def create(cls, original, custom_id=None, validate=False):
        if not custom_id:
            custom_id = cls.get_unique_short_id()
        else:
            if custom_id in ['example', 'api', 'admin', 'index']:
                raise cls.ObjectCreateError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            if cls.query.filter_by(short=custom_id).first():
                raise cls.ObjectCreateError(f'Имя "{custom_id}" уже занято.')

            if validate:
                if (
                    len(custom_id) > 16 or
                    not re.match(r'^[A-Za-z0-9]+$', custom_id)
                ):
                    raise cls.ObjectCreateError(
                        'Указано недопустимое имя для короткой ссылки'
                    )

        obj = cls(original=original, short=custom_id)
        db.session.add(obj)
        db.session.commit()
        return obj

    def get_short_url(self):
        return url_for('redirect_short', short_id=self.short, _external=True)

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_short_url()
        }
