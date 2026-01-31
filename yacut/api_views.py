from http import HTTPStatus
from flask import jsonify, request

from . import app
from .constants import NO_BODY, EMPTY_FIELD
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(NO_BODY)

    if not data.get('url'):
        raise InvalidAPIUsage(EMPTY_FIELD)

    custom_id = data.get('custom_id')

    if custom_id:
        if (
            URLMap.query.filter_by(short=custom_id).first()
            or custom_id == 'files'
        ):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

    try:

        url_map = URLMap.create(data['url'], custom_id, True)
        return jsonify(url_map.to_dict()), HTTPStatus.CREATED

    except Exception as exc:
        raise InvalidAPIUsage(str(exc))


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    result = URLMap.query.filter_by(short=short_id).first()
    if result is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': result.original}), HTTPStatus.OK
