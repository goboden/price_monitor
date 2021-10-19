from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))


class Telegram(Base):
    __tablename__ = 'telegram'

    id = Column(Integer, primary_key=True)
    username = Column(Integer, ForeignKey('users.username'), nullable=False)
    telegram_id = Column(String(64), nullable=False, unique=True)
    chat_id = Column(String(64), nullable=False)


class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer, ForeignKey('goods.id'), nullable=False)
    check_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    check_date = Column(DateTime, nullable=False)
