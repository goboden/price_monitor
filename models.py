from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float

db = declarative_base()


class Price(db):
    """
    period, goods_id (fk), price. id (pk)
    """
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    period = Column(DateTime, nullable=False)
    goods_id = Column(Integer, ForeignKey('goods.id'), nullable=False)
    price = Column(Float, nullable=False)


    def __repr__(self):
        return f'<{self.period} {self.price}>'


class Goods(db):
    """
    Поля id (pk), user_id (fk), url, check_period.
    """
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    url = Column(String, unique=True, nullable=False)
    check_period = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<{self.user_id} {self.url} {self.check_period}>'


class User(db):
    """
    id (pk), telegram_id, username, password
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(64), index=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'User {self.username}'
