from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Price(db.Model):
    """
    period, goods_id (fk), price. id (pk)
    """
    period = db.Column(db.DateTime, nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<{self.period} {self.price}>'


class Goods(db.Model):
    """
    Поля id (pk), user_id (fk), url, check_period.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    check_period = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<{self.user_id} {self.url} {self.check_period}>'


class User(db.Model, UserMixin):
    """
    id (pk), telegram_id, username, password
    """

    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'User {self.username}'
