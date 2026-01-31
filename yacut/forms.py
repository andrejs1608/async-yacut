from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut.models import URLMap


class URLMapForm(FlaskForm):
    original_link = StringField(
        "Длинная ссылка",
        validators=[DataRequired(message='Обязательное поле')],
    )
    custom_id = StringField(
        "Короткая ссылка",
        validators=[
            Optional(),
            Length(
                max=16,
                message='Короткая ссылка не длиннее 16 символов',
            ),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Разрешены только буквы и цифры',
            ),
        ],
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data:
            if URLMap.query.filter_by(short=field.data).first():
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )


class UploadFilesForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл')]
    )
    submit = SubmitField('Загрузить')
