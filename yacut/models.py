import re
from typing import Dict
from datetime import datetime

from sqlalchemy.orm import validates

from yacut import db, app
from yacut.constants import MAX_URL, MAX_SIZE, VALIDATE_URL


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL), nullable=False)
    short = db.Column(db.String(MAX_SIZE), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def is_short_url_exists(cls, short_url: str) -> bool:
        return cls.query.filter_by(short=short_url).first() is not None

    @validates('short')
    def validate_short(self, key: str, short: str) -> str:
        if not re.match(VALIDATE_URL, short):
            raise ValueError('Недопустимый формат короткой ссылки')
        return short

    def to_dict(self) -> Dict[str, str]:
        base_url = app.config['BASE_URL']
        return dict(url=self.original, short_link=f'{base_url}/{self.short}')

    def from_dict(self, data: Dict[str, str]):
        url_dict = {'url': 'original', 'custom_id': 'short'}

        for field in url_dict:
            if field in data:
                setattr(self, url_dict[field], data[field])

    def __repr__(self) -> str:
        return f'URLMap("{self.original}", "{self.short}", "{self.timestamp}")'
