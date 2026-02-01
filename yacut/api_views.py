from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import EMPTY_FIELD, NO_BODY, SHORT_NOT_FOUND
from .error_handlers import InvalidAPIUsage
from .exceptions import ObjectCreateError, ShortGenerateError
from .models import URLMap
from .utils import get_urlmap_by_short_id


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(NO_BODY)

    if not data.get('url'):
        raise InvalidAPIUsage(EMPTY_FIELD)

    custom_id = data.get('custom_id')

    try:
        url_map = URLMap.create(data['url'], custom_id, True)
        return jsonify(url_map.to_dict()), HTTPStatus.CREATED

    except (ObjectCreateError, ShortGenerateError) as exc:
        raise InvalidAPIUsage(str(exc), HTTPStatus.BAD_REQUEST)
    except Exception:
        raise InvalidAPIUsage(
            'Internal Server Error', HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    result = get_urlmap_by_short_id(short_id)
    if result is None:
        raise InvalidAPIUsage(SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)

    return jsonify({'url': result.original}), HTTPStatus.OK
