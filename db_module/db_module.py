from models import db, User, Goods, Price, Telegram
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_URI
from werkzeug.security import generate_password_hash, check_password_hash


def add_to_db(data):
    """
    Подключение к БД, добавление данных data, и запись данных в БД

    :param data: функция, возвращающая объект для добавления в БД
    :return:
    """
    def con_db(*args, **kwargs):
        engine = create_engine(DB_URI, echo=False)
        session = sessionmaker(bind=engine)
        __session = session()
        __session.add(data(*args, **kwargs))
        __session.commit()
    return con_db


@add_to_db
def add_user(username, password):
    """
    id (pk), username, password

    :param username:
    :param password: В базу сохраняется хэш пароля.
    :return:
    """
    user = User()
    return User(username=username, password=user.gen_password(password))


@add_to_db
def add_telegram_user(username, tg_username):
    """
    id (pk), username, tg_username

    :param username:
    :param tg_username:
    :return:
    """
    return Telegram(username=username, tg_username=tg_username)


@add_to_db
def add_goods(user_id, url, title, description, image, check_date):
    """
        id (pk), user_id (fk), url, title, description, image, check_period.

    :param user_id:
    :param url:
    :param title:
    :param description:
    :param image:
    :param check_date:
    :return:
    """
    return Goods(user_id=user_id, url=url, title=title,
                 description=description, image=image, check_date=check_date)


@add_to_db
def add_price(check_date, goods_id, price):
    """
    id (pk), goods_id (fk), check_date, price.

    :param check_date:
    :param goods_id:
    :param price:
    :return:
    """
    return Price(check_date=check_date, goods_id=goods_id, price=price)


def connect_db():
    engine = create_engine(DB_URI, echo=False)
    session = sessionmaker(bind=engine)
    __session = session()
    return __session


def update_password(username, new_password):
    """
    Обновление пароля в БД

    :param username:
    :param new_password:
    :return:
    """
    session = connect_db()
    user = User()
    session.query(User).filter_by(username=username).update({'password': user.gen_password(new_password)})
    session.commit()


def get_goods(username):
    """
    Получения товаров по пользователю.

    :param username:
    :return: Список кортежей
    """
    session = connect_db()
    user_id = session.query(User.id).filter_by(username=username)[0][0]
    return session.query(Goods.id,
                         Goods.title,
                         Goods.url,
                         Goods.image,
                         Goods.description,
                         Goods.check_date).filter_by(user_id=user_id).all()


if __name__ == '__main__':

    # TODO Удалить тестовые вызовы функции

    # add_user(username='test_user2', password='0987654321')
    # add_telegram_user(username='test_user1', tg_username='tg_user2')
    # add_goods(url='http://www.example4.com', check_date=datetime.now(),
    #            user_id=1, title='test goods4', description='описание', image='ссылка на картинку')
    # add_goods(url='http://www.example5.com', check_date=datetime.now(),
    #            user_id=1, title='test goods5', description='описание', image='ссылка на картинку')
    # add_goods(url='http://www.example6.com', check_date=datetime.now(),
    #            user_id=1, title='test goods6', description='описание', image='ссылка на картинку')
    # add_price(check_date=datetime.now(), goods_id=1, price=130.00)
    # add_price(check_date=datetime.now(), goods_id=1, price=1.00)
    # add_price(check_date=datetime.now(), goods_id=1, price=0.50)
    # update_password(username='test_user1', new_password='asdf')
    for i in get_goods('test_user2'):
        print(i)
    pass
