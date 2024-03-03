from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.utilis import get_unique_short_id, is_valid_custom_id
from yacut.error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def add_opinion():

    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if 'custom_id' in data and data['custom_id']:
        if (
            not is_valid_custom_id(data['custom_id'])
            or len(data['custom_id']) > 16
        ):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400
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

    db.session.add(url)

    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):

    short = URLMap.query.filter_by(short=short_id).first()
    if short is None:

        raise InvalidAPIUsage('Указанный id не найден', 404)
    url = short.original

    return jsonify({'url': url}), 200
