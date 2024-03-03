import random
import re
import string

from yacut.models import URLMap


def get_unique_short_id(custom_id=None, length=6):
    if custom_id:
        return custom_id
    else:
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(
            random.choice(characters) for _ in range(length)
        )

        if URLMap.is_short_url_exists(random_string):
            return get_unique_short_id()
        else:
            return random_string


def is_valid_custom_id(custom_id):
    return bool(re.match("^[a-zA-Z0-9]+$", custom_id))
