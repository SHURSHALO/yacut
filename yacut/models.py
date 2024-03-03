from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def is_short_url_exists(cls, short_url):
        return cls.query.filter_by(short=short_url).first() is not None

    def to_dict(self):
        return dict(
            url=self.original, short_link=f'http://localhost/{self.short}'
        )

    def from_dict(self, data):

        url_dict = {'url': 'original', 'custom_id': 'short'}

        for field in url_dict:

            if field in data:

                setattr(self, url_dict[field], data[field])

    def __repr__(self):
        return f"URLMap('{self.original}', '{self.short}', '{self.timestamp}')"
