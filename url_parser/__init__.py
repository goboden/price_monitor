from urllib.parse import urlparse
from url_parser.parser import GenegalParser
import url_parser.yandex
import url_parser.hobbygames


parsers = {
    'market.yandex.ru': url_parser.yandex,
    'hobbygames.ru': url_parser.hobbygames,
}


class ParserNotFoundError(Exception):
    def __init__(self, domain):
        self.message = f'Не найден модуль парсера для {domain}'
        super().__init__(self.message)


def get_parser(url: str, **kwargs) -> GenegalParser:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    parser_module = parsers.get(domain, False)
    if not parser_module:
        raise ParserNotFoundError(domain)
    return parser_module.Parser(url, **kwargs)
