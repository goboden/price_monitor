from sqlalchemy import create_engine
from config import DB_URI
from database.service_functions import gen_password_hash, log_to_file
import functools
from database.exceptions import *


def exception_to_log(func):
    def in_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            if func.__name__ == 'get_user_id_by_telegram_id':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_goods_by_username':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_user_by_password':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_hash_by_user':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_username_by_telegram_id':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_goods_id_by_url':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise NoGoodsError
    return in_func


@exception_to_log
def get_goods_by_username(username):
    engine = create_engine(DB_URI, echo=False)
    user_id = engine.execute(f"SELECT id FROM users WHERE username='{username}';").first()[0]
    goods = engine.execute(f"SELECT * FROM goods WHERE user_id={user_id};").all()
    return goods


@exception_to_log
def get_user_by_password(password):
    engine = create_engine(DB_URI, echo=False)
    password = gen_password(password=password)
    username = engine.execute(f"SELECT username FROM users WHERE password='{password}';").first()[0]
    return username


@exception_to_log
def get_hash_by_user(username):
    engine = create_engine(DB_URI, echo=False)
    pass_hash = engine.execute(f"SELECT password FROM users WHERE username='{username}';").first()[0]
    return pass_hash


@exception_to_log
def get_username_by_telegram_id(telegram_id):
    engine = create_engine(DB_URI, echo=False)
    username = engine.execute(f"SELECT username FROM telegram WHERE telegram_id = '{telegram_id}';").first()[0]
    return username


@exception_to_log
def get_user_id_by_telegram_id(telegram_id):
    username = get_username_by_telegram_id(telegram_id=telegram_id)
    engine = create_engine(DB_URI, echo=False)
    user_id = engine.execute(f"SELECT id FROM users WHERE username = '{username}';").first()[0]
    return user_id


@exception_to_log
def get_goods_id_by_url(url):
    engine = create_engine(DB_URI, echo=False)
    goods_id = engine.execute(f"SELECT id FROM goods WHERE url='{url}';").first()[0]
    return goods_id
