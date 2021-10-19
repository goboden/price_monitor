import os
from database import engine, session
from database.models import Base, User
from database.users import add_user
from database.exceptions import UserExistsError
import pytest


@pytest.fixture(scope='module')
def prepare(request):
    db_name = engine.url.database
    Base.metadata.create_all(engine)

    def delete_database():
        os.remove(db_name)

    request.addfinalizer(delete_database)


@pytest.mark.database
def test_create_user(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    add_user(user_name, user_telegram_id, user_chat_id)

    with pytest.raises(UserExistsError):
        add_user(user_name, user_telegram_id, user_chat_id)


    ''' with pytest.raises(TelegramUserExistsError):
        add_user(user_name, user_telegram_id, user_chat_id)

    assert True'''


@pytest.mark.database
def test_create_user1(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    with pytest.raises(UserExistsError):
        add_user(user_name, user_telegram_id, user_chat_id)
