from database.update_db import add_price_to_db, update_check_date
from database.get_from_db import get_urls_from_db
from database.orm_query import get_goods_id_by_url, get_price_by_goods_id
from url_parser import parse
from time import sleep
from datetime import datetime


def update_urls():
    urls = get_urls_from_db()

    for url in urls:
        date_time = datetime.now()
        price = parse(url[0], no_cache=True).price
        goods = get_goods_id_by_url(url[0])
        old_price = get_price_by_goods_id(goods.id)
        if price == old_price.price:
            update_check_date(old_price.id, date_time)
        else:
            add_price_to_db(date_time, goods.id, price)
        sleep(1)


if __name__ == '__main__':
    update_urls()
