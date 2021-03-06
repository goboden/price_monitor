from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

db = declarative_base()

user_goods = Table('user_goods', db.metadata,
                   Column('user_id', Integer(), ForeignKey("users.id")),
                   Column('goods_id', Integer(), ForeignKey("goods.id")))


class User(db, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    goods = relationship("Goods", secondary=user_goods, back_populates="users")


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

    prices = relationship("Price",
                          back_populates="goods",
                          order_by="Price.check_date")
    users = relationship("User", secondary=user_goods, back_populates="goods")

    @hybrid_property
    def price(self):
        return 0 if len(self.prices) == 0 else self.prices[-1].price


class Price(db):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    check_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    goods_id = Column(Integer, ForeignKey('goods.id'))
    goods = relationship("Goods", back_populates="prices")
