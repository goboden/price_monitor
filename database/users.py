from .models import User, Telegram
from . import session
from .exceptions import UserExistsError


def add_user(username, telegram_id, chat_id):
    user = session.query(User).filter_by(username=username).first()
    if user:
        raise UserExistsError
    new_user = User(username=username)
    # telegram = Telegram(username=username, telegram_id=telegram_id, chat_id=chat_id)
    session.add(new_user)
    # session.add(telegram)
    session.commit()


def get_user_by_id(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user
