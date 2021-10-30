import functools
import logging
from exceptions import *
from config import LOG_FILENAME


def log_to_file(text):
    logger = logging.getLogger('-')
    logger.setLevel(logging.ERROR)
    fh = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter(' %(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(text)


def exception_to_log(func):
    def in_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            # print(func.__name__)
            if func.__name__ == 'price_update':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise PriceException
            if func.__name__ == 'get_user_by_password':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_user_by_id':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise UserNotExistsError
            elif func.__name__ == 'get_goods_by_user':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UserOrGoodsNotExistsError
            elif func.__name__ == 'add_user':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise UserExistsError
            elif func.__name__ == 'add_goods':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-" * 100}')
                raise AddGoodsError
            if func.__name__ == 'update_urls':
                log_to_file(f' !!! {func.__name__} !!!\nОшибка:{ex}\n{"-"*100}')
                raise GoodsNotExists
            else:
                log_to_file(f' !!! {func.__name__} !!!\nException:{ex}\n{"-" * 100}')
    return in_func
