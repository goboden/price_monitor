from database import get_goods, price_update, get_chat_id_by_goods, get_goods_item
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
        price = parse_price_and_notification(goods)
        price_update(goods=goods, new_price=price)
        print('Updated:', goods.title, 'Price:', price)


def parse_price_and_notification(goods, notify_on=True):
    old_price = goods.price
    new_price = parse(goods.url, no_cache=True).price
    if notify_on:
        if new_price != old_price:
            # text = f'Изменилась цена на {goods.title}({goods.url})'
            text = f'Изменилась цена на {goods.title} ({old_price} -> {new_price})'
            for chat_id in get_chat_id_by_goods(goods):
                send_message(chat_id, text)
    return new_price


def update_price_by_goods_id(goods_id):
    """

    :param goods_id:
    :return:
    """
    goods = get_goods_item(goods_id)
    price = parse_price_and_notification(goods, notify_on=False)
    price_update(goods=goods, new_price=price)
