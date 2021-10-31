from flask import Flask, render_template, redirect, url_for, flash
from webapp.forms import LoginForm
from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user, login_required
import os
from database import get_user_by_password, get_user_by_id
from database import get_user_goods, get_goods_item, get_goods_prices
from exceptions import UserOrGoodsNotExistsError


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(32)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Для доступа к странице необходимо войти.'

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

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
            user = get_user_by_password(form.password.data)
        except UserOrGoodsNotExistsError:
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
        print(current_user.username)
        title = 'Товары'
        goods_items = get_user_goods(current_user.id)
        goods_enum = enumerate(goods_items)
        return render_template('goods_table.html',
                               page_title=title,
                               goods_enum=goods_enum)

    @app.route('/goods/<goods_id>')
    @login_required
    def goods_item(goods_id):
        goods_item = get_goods_item(goods_id)
        title = f'Товар {goods_item.title}'

        return render_template('goods_item.html',
                               page_title=title,
                               goods_item=goods_item)

    @app.route('/prices/<goods_id>')
    @login_required
    def prices(goods_id):
        goods_item = get_goods_item(goods_id)
        title = f'История цен для {goods_item.title}'
        prices = get_goods_prices(goods_id)
        prices_enum = enumerate(prices)

        return render_template('goods_prices.html',
                               page_title=title,
                               goods_item=goods_item,
                               prices_enum=prices_enum)

    return app
