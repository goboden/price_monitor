from url_parser.parsers import Parser
from url_parser.cache import HTMLCache
from url_parser.exceptions import ParseError
import pytest


def test_new_parser_class_no_methods():
    class ShopParser(Parser):
        pass

    with pytest.raises(TypeError):
        ShopParser('url')


def test_new_parser_class_with_methods():
    domain = 'shop.ru'

    @Parser.register(domain)
    class ShopParser(Parser):
        def get_price():
            pass

        def get_name():
            pass

        def get_description():
            pass

        def get_image():
            pass

    assert domain in Parser._REGISTRY


@pytest.fixture(scope='function')
def url(request):
    url = 'https://hobbygames.ru/stormfang-gunship-2014'
    html_cache = HTMLCache(url)

    def delete_cache_file():
        html_cache.delete()

    request.addfinalizer(delete_cache_file)

    return url


def test_hobbygames_fetch(url):
    parser = Parser.create(url)
    parser.parse()
    assert parser.data is not None


def test_hobbygames_discounts():
    url = 'https://hobbygames.ru/discounts'
    parser = Parser.create(url)

    with pytest.raises(ParseError):
        parser.parse()
