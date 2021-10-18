import config as cf
import os

database_name = 'test.db'
db_filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           database_name)
database_uri = 'sqlite:///' + db_filepath
cf.DB_URI = database_uri


from sqlalchemy import create_engine
from database import add_user
from database.exceptions import TelegramUserExistsError
from database.models import db
import pytest


@pytest.fixture(scope='module')
def prepare(request):
    engine = create_engine(database_uri)
    db.metadata.create_all(engine)

    def delete_database():
        os.remove(db_filepath)

    request.addfinalizer(delete_database)


@pytest.mark.database
def test_create_user(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    add_user(user_name, user_telegram_id, user_chat_id)

    with pytest.raises(TelegramUserExistsError):
        add_user(user_name, user_telegram_id, user_chat_id)

    assert True
