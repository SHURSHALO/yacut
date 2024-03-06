from typing import Tuple

from flask import jsonify, request, Response
from http import HTTPStatus

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.constants import MAX_SIZE
from yacut.utilis import db_save, get_unique_short_id, is_valid_custom_id


@app.route('/api/id/', methods=('POST',))
def add_opinion() -> Tuple[Response, int]:
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' in data and data['custom_id']:
        if (
            not is_valid_custom_id(data['custom_id'])
            or len(data['custom_id']) > MAX_SIZE
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST,
            )
        data['custom_id'] = get_unique_short_id(data['custom_id'])
    else:
        data['custom_id'] = get_unique_short_id()

    if URLMap.is_short_url_exists(data['custom_id']):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    url = URLMap()

    url.from_dict(data)

    db_save(url)

    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_url(short_id: str) -> Tuple[Response, int]:

    short = URLMap.query.filter_by(short=short_id).first()
    if short is None:

        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    url = short.original

    return jsonify({'url': url}), HTTPStatus.OK
