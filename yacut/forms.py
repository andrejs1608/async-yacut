from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (CHOOSE_FILES, FIELD_REQUIRED,
                        LINK_TAKEN, SHORT_LINK_DESC)
from .models import URLMap


class URLMapForm(FlaskForm):
    original_link = StringField(
        "Длинная ссылка",
        validators=[DataRequired(message=FIELD_REQUIRED)],
    )
    custom_id = StringField(
        "Короткая ссылка",
        validators=[
            Optional(),
            Length(
                max=16,
                message=SHORT_LINK_DESC,
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
                raise ValidationError(LINK_TAKEN)


class UploadFilesForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message=CHOOSE_FILES)]
    )
    submit = SubmitField('Загрузить')
