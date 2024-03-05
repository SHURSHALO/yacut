import re
import random

from yacut import db
from yacut.models import URLMap
from yacut.constants import CHARACTERS, VALIDATE_URL


def get_unique_short_id(custom_id: str = None, length: int = 6) -> str:
    if custom_id:
        return custom_id
    random_string = ''.join(
        random.choice(CHARACTERS) for _ in range(length)
    )

    if URLMap.is_short_url_exists(random_string):
        return get_unique_short_id()
    return random_string


def is_valid_custom_id(custom_id: str) -> bool:
    return bool(re.match(VALIDATE_URL, custom_id))


def db_save(url: URLMap):
    db.session.add(url)
    db.session.commit()
