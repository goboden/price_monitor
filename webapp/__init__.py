from flask import Flask, render_template, redirect, url_for, flash
from webapp.forms import LoginForm
from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user, login_required
import os
from database import get_user_by_password
from database import get_web_user_by_password, get_web_user_by_id
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
    # @login_required
    def goods():
        # title = f'Товары ({current_user.username})'
        title = 'Товары'
        goods_items = get_goods()
        goods_enum = enumerate(goods_items)
        return render_template('goods_table.html',
                               page_title=title,
                               goods_enum=goods_enum)

    @app.route('/goods/<goods_id>')
    # @login_required
    def goods_item(goods_id):
        # title = f'Товары ({current_user.username})'
        goods_item = get_goods_item()
        goods_name = goods_item['name']
        title = f'Товар {goods_name}'

        return render_template('goods_item.html',
                               page_title=title,
                               goods_item=goods_item)

    @app.route('/prices/<goods_id>')
    # @login_required
    def prices(goods_id):
        # title = f'Товары ({current_user.username})'
        goods_item = get_goods_item()
        goods_name = goods_item['name']
        title = f'История цен для {goods_name}'
        prices = get_prices()
        prices_enum = enumerate(prices)

        return render_template('goods_prices.html',
                               page_title=title,
                               goods_item=goods_item,
                               prices_enum=prices_enum)

    return app


def get_goods():
    goods_items = []
    for i in range(50):
        goods_item = {
            'name': f'Start Collecting! Vanguard Space Marines {i}',
            'url':
            f'https://yandex.ru/search/?clid=2186621&text=bootstrap+table+column+width&lr=2&redircnt=1634815818.1',
            'page': f'/goods/{i}',
            'price': 5859.0
        }
        goods_items.append(goods_item)
    return goods_items


def get_goods_item():
    return {
        'name':
        'Start Collecting! Vanguard Space Marines',
        'url':
        'https://hobbygames.ru/start-collecting-vanguard-space-marines',
        'price': 4000.0,
        'image':
        'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Warhammer_40k/Chaos_Space_Marines/Start-Collecting-Vanguard-Space-Marines-1024x1024-wm.jpg',
        'description':
        '''Описание

Ведите в бой элитное братство бойцов Авангарда Космического Десанта Примарис (Primaris Space Marines Vanguard) вместе с этим невероятным стартовым набором.
Внутри набора Start Collecting! Vanguard Space Marines вы найдёте:

    Лейтенанта в броне типа "Фобос" (Lieutenant in Phobos Armour), оснащённого мастерски сделанным болт-карабином "Оккулус", гравишутом и парой боевых ножей
    Три Подавителя (Suppressors), оснащенных ускорительными автопушками и гравишутами
    Три Нейтрализатора (Eliminators), оснащенных маскхалатами и снайперскими болт-винтовками
    Десять Инфильтраторов (Infiltrators), в том числе сержант отряда и адепт Спирали

К каждой миниатюре прилагается круглая подставка.
 
Правила для использования этих миниатюр вы найдёте в книге Codex: Space Marines 2019.

Обратите внимание! Миниатюры в коробке поставляются не собранными и не покрашенными. Инструкция по сборке входит в набор. 

Для сборки рекомендуем использовать специальные инструменты и клей, а окрашивать миниатюры высококачественными акриловыми красками.
'''
    }


def get_prices():
    from datetime import datetime
    prices = []
    for i in range(50):
        price = {
            'date': datetime.now(),
            'price': 5859.0
        }
        prices.append(price)
    return prices
