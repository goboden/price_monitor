from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


db = declarative_base()

user_goods = Table('user_goods', db.metadata,
                   Column('user_id', Integer(), ForeignKey("users.id")),
                   Column('goods_id', Integer(), ForeignKey("goods.id"))
                   )


class User(db):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    goods = relationship("Goods", secondary=user_goods, back_populates="user")


class Telegram(db):
    __tablename__ = 'telegram'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(64), nullable=False, unique=True)
    chat_id = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref="telegram")


class Goods(db):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)

    price = relationship("Price", back_populates="goods")
    user = relationship("User", secondary=user_goods, back_populates="goods")


class Price(db):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    check_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    goods_id = Column(Integer, ForeignKey('goods.id'))

    goods = relationship("Goods", back_populates="price")
