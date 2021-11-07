from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import DB_URI
from database.models import db, User, Telegram, Goods, Price
from database import generate_hash
from datetime import datetime, timedelta

engine = create_engine(DB_URI)
session = scoped_session(sessionmaker(bind=engine))


def create_db():
    db.metadata.create_all(engine)


def add_users():
    users = (
        (1, 'Test User 1', 1234567890, 11032511, '1'),
        (2, 'Test User 2', 1234567891, 11032511, '2'),
        (3, 'Test User 3', 1234567892, 11032511, '3'),
        (4, 'Test User 4', 1234567893, 11032511, '4'),
    )
    for user in users:
        add_user(*user)


def add_goods(goods):
    for goods_item in goods:
        add_goods_item(*goods_item)


def add_user(id, name, telegram_id, chat_id, password):
    print(f'{id}, {name}, {telegram_id}, {chat_id}, {password}')
    telegram = Telegram(telegram_id=telegram_id, chat_id=chat_id)
    telegram.user_id = id
    user = User(id=id, username=name, password=generate_hash(password))
    session.add(telegram)
    session.add(user)
    session.commit()


def add_goods_item(id, user_id, title, url, image, description, price):
    print(f'{id}, {user_id}, {title}, {price}')

    user = session.query(User).filter_by(id=user_id).first()
    goods_item = session.query(Goods).filter_by(url=url).first()
    if not goods_item:
        goods_item = Goods(id=id,
                           title=title,
                           url=url,
                           image=image,
                           description=description)
    goods_item.users.append(user)
    session.add(goods_item)
    for minutes in range(1, 10):
        price_item = Price(check_date=datetime.now() -
                           timedelta(minutes=minutes),
                           price=(price - minutes * 100))
        price_item.goods = goods_item
        session.add(price_item)
    session.commit()


goods = (
    (1, 1, 'Warhammer 40,000: Recruit Edition',
     'https://hobbygames.ru/warhammer-40000-recruit-edition',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Warhammer_40k/Starter/WH40k_Recruit_Edition_Starter-1024x1024-wm.jpg',
     'Описание', 3100.0),
    (2, 1, 'Start Collecting! Chaos Space Marines',
     'https://hobbygames.ru/start-collecting-chaos-space-marines-2019',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Warhammer_40k/Chaos_Space_Marines/Start-Collecting-Chaos-Space-Marines-1024x1024-wm.jpg',
     'Описание', 5700.0),
    (3, 1, 'Combat Patrol: Space Marines',
     'https://hobbygames.ru/combat-patrol-space-marines',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Warhammer_40k/Space_Marines/HG/WH40k_SM_Combat_Patrol-1024x1024-wm.jpg',
     'Описание', 8200.0),
    (4, 1, 'Necron Warriors and Paint Set',
     'https://hobbygames.ru/necron-warriors-and-paint-set',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Paints/Set_and_Instrument/WH40k_Necron_Warriors_Paints_Set-1024x1024-wm.jpg',
     'Описание', 2100.0),
    (5, 1, 'Combat Patrol: Dark Angels',
     'https://hobbygames.ru/combat-patrol-dark-angels',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Temp/300121/Combat_Patrol_Dark_Angels-1024x1024-wm.jpg',
     'Описание', 8100.0),
    (6, 2, 'Warhammer 40,000: Recruit Edition',
     'https://hobbygames.ru/warhammer-40000-recruit-edition',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Warhammer_40k/Starter/WH40k_Recruit_Edition_Starter-1024x1024-wm.jpg',
     'Описание', 3100.0),
    (7, 3, 'Warhammer 40,000: Recruit Edition',
     'https://hobbygames.ru/warhammer-40000-recruit-edition',
     'https://hobbygames.cdnvideo.ru/image/cache/hobbygames_beta/data/Games_Workshop_New/Warhammer_40k/Starter/WH40k_Recruit_Edition_Starter-1024x1024-wm.jpg',
     'Описание', 3100.0),
)

if __name__ == "__main__":
    print('Init start')
    create_db()
    print('Database created')

    add_users()
    print('Users added')
    add_goods(goods)
    print('Goods added')
    print('Init complete')
