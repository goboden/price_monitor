from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = StringField('Пароль',
                          validators=[DataRequired()],
                          render_kw={"class": "form-control"})
    submit = SubmitField('Отправить')
