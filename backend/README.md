**update_urls()** - Читает список товаров и по урлам проверяет изменение цены. Если цена не изменилась, обновляет дату на последней записи. Если цена изменилась, добавляет новую цену в БД.

**parse_price_and_notification(goods, notify_on=True)** - Оповещение пользователей об изменении цены на товары.

**update_price_by_goods_id(goods_id)** - Обновляет цены на товары пользователя.
