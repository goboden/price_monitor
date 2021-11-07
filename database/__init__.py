from hashlib import scrypt
from random import shuffle, choice
from config import DB_URI, PASSWORD_LENGHT, SALT
from sqlalchemy import create_engine
from .models import db, User, Telegram, Goods, Price
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import *
from decorators import exception_to_log


engine = create_engine(DB_URI)
session = Session(bind=engine)


@exception_to_log
def create_db():
    db.metadata.create_all(engine)


@exception_to_log
def drop_db():
    db.metadata.drop_all(engine)


@exception_to_log
def check_password(username, password):
    """

    :param username:
    :param password:
    :return:
    """
    hash_from_db = session.query(User).filter(User.username == username).first().password
    # telegram_id = session.query(User).filter(User.username == username).first().telegram[0].id
    if generate_hash(password) == hash_from_db:
        return True
    else:
        return False


@exception_to_log
def generate_password(telegram_id):
    """
        Update password in database and return generated password
    :param telegram_id:
    :return: generated password
    """
    password = password_generator(PASSWORD_LENGHT)
    username = session.query(Telegram).filter(Telegram.telegram_id == telegram_id).first().user.username
    session.query(User).filter_by(username=username).update({'password':
                                                            generate_hash(password=password)})
    session.commit()
    return password


@exception_to_log
def password_generator(password_length=15):
    alphabet = list('1234567890+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    shuffle(alphabet)
    password = ''.join([choice(alphabet) for _ in range(password_length)])
    return password


@exception_to_log
def generate_hash(password, salt=SALT):
    return scrypt(str(password).encode(), salt=str(salt).encode(), n=8, r=256, p=4, dklen=64).hex()


@exception_to_log
def get_user_by_password(password):
    """

    :param password:
    :return:
    """
    return session.query(User).filter(User.password == generate_hash(password)).first()


@exception_to_log
def get_user_by_id(user_id):
    """

    :param user_id:
    :return:
    """
    return session.query(User).filter(User.id == user_id).first()


@exception_to_log
def get_goods_by_user(username):
    """

    :param username:
    :return:
    """
    return session.query(User).filter(User.username == username).first().goods


@exception_to_log
def add_user(username, telegram_id, chat_id, password):
    """

    :param username:
    :param telegram_id:
    :param chat_id:
    :param password:
    :return:
    """
    user = User(
        username=username,
        password=generate_hash(password=password)
    )
    session.add(user)
    session.flush()

    telegram = Telegram(
        telegram_id=telegram_id,
        chat_id=chat_id,
        user_id=user.id
    )
    session.add(telegram)
    session.commit()


@exception_to_log
def add_goods(user: object, url, title, description, image_url, price):
    """

    :param user:
    :param url:
    :param title:
    :param description:
    :param image_url:
    :param price:
    :return:
    """
    goods_exist = (session.query(Goods).filter(Goods.url == url).first() is None)

    if goods_exist:
        goods = Goods(
            url=url,
            title=title,
            description=description,
            image=image_url,
        )
        goods.user.append(user)
        session.add(goods)
        session.flush()

        price = Price(
            check_date=datetime.now(),
            price=price,
            goods_id=goods.id
        )
        session.add(price)
        session.commit()
    else:
        goods = session.query(Goods).filter(Goods.url == url).first()
        user.goods.append(goods)
        session.add(user)
        session.commit()


@exception_to_log
def price_update(goods: object, new_price: float):
    """

    :param goods:
    :param new_price:
    :return:
    """
    if goods.price[-1].price != float(new_price):
        price = Price(
            check_date=datetime.now(),
            price=new_price,
            goods_id=goods.id
        )
        session.add(price)
    else:
        goods.price[-1].check_date = datetime.now()

    session.commit()


@exception_to_log
def get_goods():
    return session.query(Goods).all()


def get_user_goods(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user.goods


def get_goods_item(goods_id):
    return session.query(Goods).filter_by(id=goods_id).first()


def get_goods_prices(goods_id):
    prices = session.query(Price).filter_by(goods_id=goods_id)
    prices = prices.order_by(Price.check_date)
    return prices


def get_chat_id_by_goods(goods):
    """

    :param goods:
    :return: list of chat id
    """
    chat_ids = []
    for tg_user in goods.user:
        chat_ids.append(tg_user.telegram[0].chat_id)
    return chat_ids
