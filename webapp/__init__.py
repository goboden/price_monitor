from flask import Flask, render_template, redirect, url_for, flash
from webapp.forms import LoginForm
from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user, login_required
import os
from database import get_user_by_password, get_web_user_by_password, get_web_user_by_id
from database.exceptions import UserNotExistsError


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(32)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Для доступа к странице необходимо войти.'

    @login_manager.user_loader
    def load_user(user_id):
        return get_web_user_by_id(user_id)

    @app.route('/')
    def index():
        return redirect(url_for('goods'))

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process_login', methods=['POST'])
    def process_login():
        form = LoginForm()
        try:
            # user = get_user_by_password(form.password.data)
            user = get_web_user_by_password(form.password.data)
        except UserNotExistsError:
            user = None  # ???
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Вы указали неправильный пароль.')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/goods')
    @login_required
    def goods():
        title = f'Товары ({current_user.username})'
        return render_template('goods.html', page_title=title)

    return app
