from database import get_goods, price_update
from url_parser import parse
from decorators import exception_to_log


@exception_to_log
def update_urls():
    """

    :return:
    """
    all_goods = get_goods()

    for goods in all_goods:
        price = parse(goods.url, no_cache=True).price
        price_update(goods=goods, new_price=price)
