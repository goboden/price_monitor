import os
from database import engine, session
from database.models import Base, User, Telegram, Goods, Price
from database import users
from database.exceptions import UserExistsError
from datetime import datetime, timedelta
import pytest


@pytest.fixture(scope='module')
def prepare(request):
    db_name = engine.url.database
    Base.metadata.create_all(engine)

    yield

    session.close()
    #os.remove(db_name)


@pytest.mark.database
def test_create_objects(prepare):
    print(' ')
    telegram = Telegram(id=1234567890, name='@user', chat_id=987654321)
    user = User(name='SampleUser')
    telegram.user = user
    session.add(user)

    another_user = User(name='AnotherUser')
    session.add(another_user)

    goods = Goods(url='http://goods.ru/g1', name='G1')
    goods.users.append(user)
    goods.users.append(another_user)
    session.add(goods)

    price1 = Price(date=datetime.now(), price=100)
    goods.prices.append(price1)
    price2 = Price(date=(datetime.now() + timedelta(minutes=1)), price=200)
    goods.prices.append(price2)
    session.add_all((price1, price2))

    session.commit()

    user = session.query(Telegram).filter_by(id=1234567890).first().user
    print(f'user={user.name}')
    for goods_item in user.goods:
        print(f' ... goods={goods_item.name} ({goods_item.url})')
        for price_record in goods.prices:
            print(f' ... ... price={price_record.price}')
        for goods_user in goods.users:
            print(f' ... ... user={goods_user.name}')


@pytest.mark.database
def qtest_create_user1(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    users.add(user_name, user_telegram_id, user_chat_id)


@pytest.mark.database
def qtest_create_user1_twice(prepare):
    user_name = '@test_user'
    user_telegram_id = 123456789
    user_chat_id = 987654321

    with pytest.raises(UserExistsError):
        users.add(user_name, user_telegram_id, user_chat_id)


@pytest.mark.database
def qtest_create_user2(prepare):
    users.add('@test_user2', 123456700, 1000654321)


@pytest.mark.database
def qtest_create_user3(prepare):
    users.add('@test_user3', 123456701, 1000654321)


@pytest.mark.database
def qtest_get_user_by_telegram_id(prepare):
    user_telegram_id = 123456700
    user = users.get_by_teleram_id(user_telegram_id)
    assert user.telegram.chat_id == 1000654321
    # print(f'Telegram user: {user.name} / {user.telegram.chat_id}')


@pytest.mark.database
def qtest_password(prepare):
    telegram_id = 123456700
    password = users.new_password_from_telegram(telegram_id)
    user = users.get_by_password(password)
    assert user.telegram.id == telegram_id
