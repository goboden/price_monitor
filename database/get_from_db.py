from database.service_functions import gen_password_hash
from database.exceptions import *
from database.decorators import *


@get_from_db
def __get_user_id(username):
    return f"SELECT id FROM users WHERE username='{username}';"


@get_from_db
def get_goods_by_username(username):
    user_id = __get_user_id(username)[0][0]
    return f"SELECT * FROM goods WHERE user_id={user_id};"


@get_from_db
def get_user_by_password_(password):
    password = gen_password_hash(password=password)
    return f"SELECT username FROM users WHERE password='{password}';"


@get_from_db
def get_hash_by_user(username):
    return f"SELECT password FROM users WHERE username='{username}';"


@get_from_db
def get_username_by_telegram_id(telegram_id):
    return f"SELECT username FROM telegram WHERE telegram_id = '{telegram_id}';"


@get_from_db
def get_user_id_by_telegram_id(telegram_id):
    username = get_username_by_telegram_id(telegram_id=telegram_id)[0][0]
    return f"SELECT id FROM users WHERE username = '{username}';"


@get_from_db
def get_urls_from_db():
    return "SELECT url FROM goods;"


@get_from_db
def get_goods_id_by_url(url):
    return f"SELECT id FROM goods WHERE url='{url}';"
