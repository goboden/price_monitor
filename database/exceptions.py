class UserExistsError(Exception):
    """Пользователь уже есть в базе"""


class UserNotExistsError(Exception):
    """Пользователя нет в базе"""


class EmptyUsername(Exception):
    """Имя пользователя пустое"""


class TelegramUserExistsError(Exception):
    """Пользователь уже есть в базе"""


class UrlIsEmpty(Exception):
    """Пустой URL не допустим"""


class PriceException(Exception):
    """Что-то не то с ценой. Смотри логи."""


class PasswordException(Exception):
    """Что-то не то с пользователем. Смотри логи."""

class NoGoodsError(Exception):
    """Нет товара с таким URL в базе"""
