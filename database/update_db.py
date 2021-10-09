from database.models import db, User, Goods, Price, Telegram
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_URI, SECRET_KEY
import hashlib
from database.service_functions import gen_password


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
    return User(username=username, password=gen_password(password))


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
    session.query(User).filter_by(username=username).update({'password': gen_password(password=new_password)})
    session.commit()
