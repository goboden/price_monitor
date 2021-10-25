from database.exceptions import *
from sqlalchemy import create_engine
from database.models import User, Goods, Telegram, Price
from sqlalchemy.orm import scoped_session, sessionmaker
from config import DB_URI
from service_functions import gen_password_hash


def connect_to_db():
    engine = create_engine(DB_URI)
    session = scoped_session(sessionmaker(bind=engine))
    return session


def get_web_user_by_password(password):
    session = connect_to_db()
    hashed = gen_password_hash(password)
    user = session.query(User).filter(User.password == hashed).all()
    return user


def get_web_user_by_id(user_id):
    session = connect_to_db()
    user = session.query(User).filter(User.id == user_id).first()
    return user


def get_goods_id_by_url(url):
    session = connect_to_db()
    goods = session.query(Goods).filter(Goods.url == url).first()
    return goods


def get_user_id_by_telegram_id(telegram_id):
    session = connect_to_db()
    username = session.query(Telegram.username).filter_by(telegram_id=telegram_id).first()[0]
    user_id = session.query(User.id).filter_by(username=username).first()[0]
    return user_id


def get_price_by_goods_id(goods_id):
    session = connect_to_db()
    price = session.query(Price).filter(Price.goods_id == goods_id).all()[-1]
    return price
