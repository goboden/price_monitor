from sqlalchemy import create_engine
# from database.models import User
from config import DB_URI
from database.service_functions import gen_password


def get_goods_by_username(username):
    engine = create_engine(DB_URI, echo=False)
    user_id = engine.execute(f"SELECT id FROM users WHERE username='{username}';").first()[0]
    goods = engine.execute(f"SELECT * FROM goods WHERE user_id={user_id};").all()
    return goods


def get_user_by_password(password):
    engine = create_engine(DB_URI, echo=False)
    password = gen_password(password=password)
    username = engine.execute(f"SELECT username FROM users WHERE password='{password}';").first()[0]
    return username


def get_hash_by_user(username):
    engine = create_engine(DB_URI, echo=False)
    pass_hash = engine.execute(f"SELECT password FROM users WHERE username='{username}';").first()[0]
    return pass_hash
