class UserExistsError(Exception):
    """Пользователь уже есть в базе"""


class UserOrGoodsNotExistsError(Exception):
    """Товара нет в базе или у пользователя нет товаров"""


class TelegramUserExistsError(Exception):
    """Пользователь уже есть в базе"""


class PriceException(Exception):
    """Что-то не то с ценой. Смотри логи."""


class PasswordException(Exception):
    """Что-то не то с пользователем. Смотри логи."""


class AddGoodsError(Exception):
    """Ошибка при добавлении товара"""


class GoodsNotExists(Exception):
    """Видимо url не верный"""


class URLExistsError(Exception):
    pass
