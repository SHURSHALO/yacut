import re
import random

from yacut import db
from yacut.models import URLMap
from yacut.constants import CHARACTERS


def get_unique_short_id(custom_id=None, length=6):
    if custom_id:
        return custom_id
    else:
        random_string = ''.join(
            random.choice(CHARACTERS) for _ in range(length)
        )

        if URLMap.is_short_url_exists(random_string):
            return get_unique_short_id()
        return random_string


def is_valid_custom_id(custom_id):
    return bool(re.match("^[a-zA-Z0-9]+$", custom_id))


def bd_save(url):
    db.session.add(url) 
    db.session.commit()
