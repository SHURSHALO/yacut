from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL

from yacut.constants import MAX_URL, MAX_SIZE


class UrlForm(FlaskForm):

    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_URL),
            URL(message="Введите правильный URL"),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[Length(1, MAX_SIZE), Optional()]
    )
    submit = SubmitField('Создать')
