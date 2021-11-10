from hashlib import scrypt
from random import shuffle, choice
from config import DB_URI, PASSWORD_LENGHT, SALT
from sqlalchemy import create_engine
from .models import db, User, Telegram, Goods, Price
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from sqlalchemy.exc import *
from decorators import exception_to_log
from exceptions import URLExistsError, TelegramUserNotExistsError

engine = create_engine(DB_URI, connect_args={'check_same_thread': False})
session = scoped_session(sessionmaker(bind=engine))


@exception_to_log
def create_db():
    db.metadata.create_all(engine)
    print('Database created')


@exception_to_log
def drop_db():
    db.metadata.drop_all(engine)
    print('Database deleted')


@exception_to_log
def generate_password(telegram_id):
    """
        Update password in database and return generated password
    :param telegram_id:
    :return: generated password
    """
    password = password_generator(PASSWORD_LENGHT)
    hashed = generate_hash(password)
    telegram = session.query(Telegram).filter_by(
        telegram_id=telegram_id).first()
    if telegram:
        telegram.user.password = hashed
        session.commit()
        return password
    else:
        raise TelegramUserNotExistsError


@exception_to_log
def password_generator(password_length=15):
    alphabet = list(
        '1234567890+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )
    shuffle(alphabet)
    password = ''.join([choice(alphabet) for _ in range(password_length)])
    return password


@exception_to_log
def generate_hash(password, salt=SALT):
    return scrypt(str(password).encode(),
                  salt=str(salt).encode(),
                  n=8,
                  r=256,
                  p=4,
                  dklen=64).hex()


@exception_to_log
def get_user_by_password(password):
    """

    :param password:
    :return:
    """
    return session.query(User).filter(
        User.password == generate_hash(password)).first()


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
def add_user(username, telegram_id, chat_id):
    """

    :param username:
    :param telegram_id:
    :param chat_id:
    :param password:
    :return:
    """
    user = User(username=username)
    session.add(user)
    session.flush()

    telegram = Telegram(telegram_id=telegram_id,
                        chat_id=chat_id,
                        user_id=user.id)
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
    goods_exist = (session.query(Goods).filter(Goods.url == url).first() is
                   None)

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

        price = Price(check_date=datetime.now(),
                      price=price,
                      goods_id=goods.id)
        session.add(price)
        session.commit()
    else:
        goods = session.query(Goods).filter(Goods.url == url).first()
        user.goods.append(goods)
        session.add(user)
        session.commit()


def add_url(telegram_id, url, title, description, image, price):
    telegram = session.query(Telegram).filter_by(
        telegram_id=telegram_id).first()
    user = telegram.user
    if user:
        goods_item = session.query(Goods).filter_by(url=url).first()
        if not goods_item:
            goods_item = Goods(url=url,
                               title=title,
                               description=description,
                               image=image)
            price = Price(check_date=datetime.now(), price=price)
            goods_item.prices.append(price)
            session.add(goods_item)
        if goods_item not in user.goods:
            user.goods.append(goods_item)
            session.add(user)
        else:
            raise URLExistsError
        session.commit()


@exception_to_log
def price_update(goods: object, new_price: float):
    """

    :param goods:
    :param new_price:
    :return:
    """
    if goods.price != new_price:
        prices = Price(check_date=datetime.now(),
                      price=new_price,
                      goods_id=goods.id)
        session.add(prices)
    else:
        goods.prices[-1].check_date = datetime.now()

    session.commit()


# @exception_to_log
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
    for tg_user in goods.users:
        chat_ids.append(tg_user.telegram[0].chat_id)
    return chat_ids
