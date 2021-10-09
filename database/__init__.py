from sqlalchemy import create_engine

import database.models
from config import DB_URI
from database.update_db import add_user, add_telegram_user, add_price, add_goods, update_password
from database.get_from_db import get_hash_by_user, get_user_by_password, get_goods_by_username
from database.service_functions import gen_password


def check_password(username, password):
    hash_from_db = get_hash_by_user(username)
    if gen_password(password) == hash_from_db:
        return True
    else:
        return False