import random
import string

from .constants import MAX_GENERATE_ATTEMPTS, SHORT_ID_LENGTH, UNIQUE_ID_ERROR
from .exceptions import ShortGenerateError


def get_unique_short_id():
    from .models import URLMap
    chars = string.ascii_letters + string.digits
    for _ in range(MAX_GENERATE_ATTEMPTS):
        short_id = ''.join(random.choices(chars, k=SHORT_ID_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id

    raise ShortGenerateError(UNIQUE_ID_ERROR)


def get_urlmap_by_short_id(short_id):
    from .models import URLMap
    return URLMap.query.filter_by(short=short_id).first()
