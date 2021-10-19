from .models import User, Telegram
from . import session
from .exceptions import UserExistsError


def add(name, telegram_id, chat_id):
    user = session.query(User).filter_by(name=name).first()
    if not user:
        new_user = User(name=name)
        telegram = Telegram(id=telegram_id, chat_id=chat_id)
        new_user.telegram.append(telegram)
        session.add(new_user)
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
    pass
