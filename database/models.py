from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    telegram = relationship('Telegram', backref='user')


class Telegram(Base):
    __tablename__ = 'telegram'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    #user = relationship('User', back_populates='telegram')


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
