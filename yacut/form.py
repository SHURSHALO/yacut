from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class UrlForm(FlaskForm):

    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message="Введите правильный URL"),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
