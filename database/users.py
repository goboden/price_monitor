from .models import User, Telegram
from . import session
from .exceptions import UserExistsError


def add(name, telegram_id, chat_id):
    telegram = session.query(Telegram).filter_by(id=telegram_id).first()
    if not telegram:
        telegram = Telegram(id=telegram_id, name=name, chat_id=chat_id)
        user = User(name=name)
        telegram.user = user
        session.add(user)
        session.commit()
    else:
        raise UserExistsError


def get_by_id(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def get_by_teleram_id(telegram_id):
    user = session.query(Telegram).filter_by(id=telegram_id).first().user
    return user


def get_by_password(password):
    hashed = password
    user = session.query(User).filter_by(password=hashed).first()
    return user


def new_password_from_telegram(telegram_id):
    password = 'PASS'
    hashed = password
    user = session.query(Telegram).filter_by(id=telegram_id).first().user
    user.password = hashed
    session.commit()
    return password
