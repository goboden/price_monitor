from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

db = declarative_base()


class Price(db):
    """
    id (pk), goods_id (fk), check_date, price.
    """
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    goods_id = Column(Integer, ForeignKey('goods.id'), nullable=False)
    check_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)


class Goods(db):
    """
    id (pk), user_id (fk), url, title, description, image, check_date.

    """
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    check_date = Column(DateTime, nullable=False)


class User(db):
    """
    id (pk), username, password
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))

    def gen_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Telegram(db):
    """
    id (pk), username, tg_username
    """
    __tablename__ = 'telegram'

    id = Column(Integer, primary_key=True)
    username = Column(Integer, ForeignKey('users.username'), nullable=False)
    tg_username = Column(String(64), nullable=False, unique=True)
