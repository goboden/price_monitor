import os
from database import engine, session
from database.models import Base, User
from database import users
from database.exceptions import UserExistsError
import pytest


@pytest.fixture(scope='module')
def prepare(request):
    db_name = engine.url.database
    Base.metadata.create_all(engine)

    yield

    session.close()
    # os.remove(db_name)


@pytest.mark.database
def test_create_user(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    users.add(user_name, user_telegram_id, user_chat_id)


@pytest.mark.database
def test_create_user1(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    with pytest.raises(UserExistsError):
        users.add(user_name, user_telegram_id, user_chat_id)


@pytest.mark.database
def test_create_user2(prepare):
    user_name = '@test_user2'
    user_telegram_id = 123456700
    user_chat_id = 1000654321

    users.add(user_name, user_telegram_id, user_chat_id)


@pytest.mark.database
def test_create_user3(prepare):
    users.add('@test_user3', 123456701, 1000654321)


@pytest.mark.database
def test_get_user_by_telegram_id(prepare):
    user_telegram_id = 123456700
    user = users.get_by_teleram_id(user_telegram_id)
    print(f'Telegram user {user.name}')
