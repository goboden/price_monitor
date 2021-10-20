from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy import Table, UniqueConstraint
from sqlalchemy.orm import relationship
from flask_login import UserMixin


Base = declarative_base()

user_goods_table = Table('user_goods', Base.metadata,
                         Column('user_id', ForeignKey('users.id')),
                         Column('goods_id', ForeignKey('goods.id')))


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    password = Column(String(128), unique=True)
    telegram = relationship('Telegram', back_populates='user', uselist=False)
    goods = relationship('Goods',
                         secondary=user_goods_table,
                         back_populates='users')


class Telegram(Base):
    __tablename__ = 'telegram'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='telegram')


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    users = relationship('User',
                         secondary=user_goods_table,
                         back_populates='goods')
    prices = relationship('Price')


class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer, ForeignKey('goods.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint('goods_id', 'date'), )
