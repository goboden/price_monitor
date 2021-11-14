from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    password = StringField('Пароль',
                           validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    remember = BooleanField('Запомнить',
                            render_kw={
                                'class': 'form-check-input',
                                'type': 'checkbox',
                            })
    submit = SubmitField('Войти',
                         render_kw={'class': 'btn btn-outline-primary'})
