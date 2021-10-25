from sqlalchemy import create_engine
from config import DB_URI
from service_functions import log_to_file
from database.exceptions import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import functools


def get_from_db(func):
    @exception_to_log
    def data(*args, **kwargs):
        engine = create_engine(DB_URI, echo=False)
        query = engine.execute(func(*args, **kwargs)).all()
        return query
    return data


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
            if func.__name__ == 'add_user':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UserExistsError
            elif func.__name__ == 'add_telegram_user_to_db':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise TelegramUserExistsError
            elif func.__name__ == 'add_goods_to_db':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UrlError
            elif func.__name__ == 'add_price_to_db':
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
