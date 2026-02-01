import re
from datetime import datetime

from flask import url_for

from . import db
from .constants import (INVALID_SHORT_ID, LINK_TAKEN,
                        ORIGINAL_URL_SIZE, SHORT_URL_SIZE)
from .exceptions import ObjectCreateError
from .utils import get_unique_short_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_SIZE), nullable=False)
    short = db.Column(db.String(SHORT_URL_SIZE), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def create(cls, original, custom_id=None, validate=False):
        if not custom_id:
            custom_id = get_unique_short_id()
        else:
            if custom_id == 'files':
                raise ObjectCreateError(LINK_TAKEN)

            if cls.query.filter_by(short=custom_id).first():
                raise ObjectCreateError(LINK_TAKEN)

            if validate:
                if (
                    len(custom_id) > SHORT_URL_SIZE or
                    not re.match(r'^[A-Za-z0-9]+$', custom_id)
                ):
                    raise ObjectCreateError(INVALID_SHORT_ID)

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
