from database.models import db, User, Goods, Price, Telegram
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from config import DB_URI, SECRET_KEY
import hashlib
from database.service_functions import gen_password_hash, log_to_file
import functools
from database.exceptions import *


def exception_to_log(func):

    def in_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            if func.__name__ == 'add_user':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise UserExistsError
            elif func.__name__ == 'add_telegram_user_to_db':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise TelegramUserExistsError
            elif func.__name__ == 'add_goods':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UrlIsEmpty
            elif func.__name__ == 'add_price':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise PriceException
            elif func.__name__ == 'update_password':
                log_to_file(f'!!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise PasswordException
    return in_func


def add_to_db(data):
    """
    Подключение к БД, добавление данных data, и запись данных в БД

    :param data: функция, возвращающая объект для добавления в БД
    :return:
    """

    @exception_to_log
    @functools.wraps(data)
    def con_db(*args, **kwargs):
        engine = create_engine(DB_URI, echo=False)
        session = sessionmaker(bind=engine)
        __session = session()
        __session.add(data(*args, **kwargs))
        __session.commit()
    return con_db


@add_to_db
def add_user_to_db(username, password='0000'):
    """
    id (pk), username, password

    :param username:
    :param password: В базу сохраняется хэш пароля.
    :return:
    """
    return User(username=username, password=gen_password_hash(password))


@add_to_db
def add_telegram_user_to_db(username, telegram_id, chat_id):
    """
    id (pk), username, tg_username

    :param username:
    :param tg_username:
    :param chat_id:
    :return:
    """
    return Telegram(username=username, telegram_id=telegram_id, chat_id=chat_id)


@add_to_db
def add_goods_to_db(user_id, url,  check_date, title='', description='', image=''):
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
def add_price_to_db(check_date, goods_id, price):
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


@exception_to_log
def update_password(username, new_password):
    """
    Обновление пароля в БД

    :param username:
    :param new_password:
    :return:
    """
    session = connect_db()

    if username == '':
        raise EmptyUsername("Имя пользователя не может быть пустым!")
    elif session.query(User.username).filter_by(username=username).first() is None:
        raise UserNotExistsError("Такого пользователя в базе нет!")
    elif new_password == '':
        raise PasswordException("Не стоит использовать пустой пароль!")

    session.query(User).filter_by(username=username).update({'password': gen_password_hash(password=new_password)})
    session.commit()
