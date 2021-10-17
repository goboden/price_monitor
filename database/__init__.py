import datetime
from database.exceptions import *
from sqlalchemy import create_engine
from random import random
import database.models
from config import PASSWORD_LENGHT
from database.update_db import add_user_to_db, add_telegram_user_to_db, \
    add_price_to_db, add_goods_to_db, update_password
from database.get_from_db import get_hash_by_user, get_goods_id_by_url
from database.service_functions import gen_password_hash, log_to_file, password_generator


def check_password(username, password):
    hash_from_db = get_hash_by_user(username)[0][0]
    if gen_password_hash(password) == hash_from_db:
        return True
    else:
        return False


def add_user(username, telegram_id, chat_id):
    add_user_to_db(username=username)
    add_telegram_user_to_db(username=username, telegram_id=telegram_id, chat_id=chat_id)


def generate_password(telegram_id):
    password = password_generator(PASSWORD_LENGHT)
    username = get_from_db.get_username_by_telegram_id(telegram_id)[0][0]
    update_password(username=username, new_password=password)
    return password


def generate_hash(password, salt):
    return gen_password_hash(password=password, salt=salt)


def add_url(telegram_id, url, price):
    if url == '':
        log_to_file(f' !!! add_url !!!\nОшибка: URL не может быть пустым\n{"-" * 100}')
        raise UrlError('URL не может быть пустым')

    check_date = datetime.datetime.now()
    user_id = get_from_db.get_user_id_by_telegram_id(telegram_id=telegram_id)[0][0]
    add_goods_to_db(user_id=user_id, url=url, check_date=check_date)
    goods_id = get_goods_id_by_url(url)[0][0]
    add_price_to_db(check_date=check_date, goods_id=goods_id, price=price)
