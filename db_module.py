from models import db, User, Goods, Price
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_URI
from werkzeug.security import generate_password_hash, check_password_hash

def add_to_db(data):
    """
    Поодключение к БД, добавление данных data, и запись данных в БД

    :param data: функция, возвращающая объект для добавления в БД
    :return:
    """
    def con_db(*args, **kwargs):
        engine = create_engine(DB_URI, echo=False)
        session = sessionmaker(bind=engine)
        __session = session()
        __session.add(data(*args, **kwargs))
        __session.commit()
    return con_db


@add_to_db
def add_user(telegram_id, username, password):
    user = User()
    return User(telegram_id=telegram_id, username=username, password=user.set_password(password))


@add_to_db
def add_goods(url, check_period, user_id):
    return Goods(url=url, check_period=check_period, user_id=user_id)


@add_to_db
def add_price(period, goods_id, price):
    return Price(period=period, goods_id=goods_id, price=price)


if __name__ == '__main__':

    # TODO Удалить тестовые вызовы функции

    # add_user(telegram_id='tg2', username='test_user6', password='0123456789')
    # add_goods(url='http://www.example.com', check_period=datetime.now(), user_id=2)
    # add_price(period=datetime.now(), goods_id=1, price=13.13)
    pass
