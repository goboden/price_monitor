from database import get_goods, price_update, get_last_price, get_chat_id_by_goods
from url_parser import parse
from decorators import exception_to_log
from telebot import send_message


@exception_to_log
def update_urls():
    """

    :return:
    """
    all_goods = get_goods()

    for goods in all_goods:
        price = price_notification(goods)
        price_update(goods=goods, new_price=price)
        print('Updated:', goods.title, 'Price:', price)


def price_notification(goods):
    old_price = get_last_price(goods).price.last_price.price
    new_price = parse(goods.url, no_cache=True).price
    if new_price != old_price:
        text = f'Изменилась цена на {goods.title}'
        for chat_id in get_chat_id_by_goods(goods):
            send_message(chat_id, text)
    return new_price
