import url_parser
from url_parser.exceptions import BadURLError, ParserNotFoundError
from url_parser.exceptions import FetchError, ParseError
import pytest


@pytest.mark.parametrize('url, exception',
                         [('hobbygames.ru', BadURLError),
                          ('https://hobbygames.com', ParserNotFoundError),
                          ('https://hobbygames.ru/corvus-error', FetchError),
                          ('https://market.yandex.ru/product--a', FetchError),
                          ('https://hobbygames.ru', ParseError)])
def test_parser_init(url, exception):
    with pytest.raises(exception):
        url_parser.parse(url)


@pytest.mark.parametrize('url',
                         ['https://hobbygames.ru/codex-deathwatch-hardback',
                          'https://hobbygames.ru/corvus-blackstar'])
def test_fetch(url):
    data = url_parser.parse(url)
    assert data is not None


@pytest.mark.parametrize('url, name', [
    ('https://hobbygames.ru/codex-deathwatch-hardback',
     'Codex: Deathwatch 8th edition (Hardback)'),
    ('https://hobbygames.ru/corvus-blackstar', 'Corvus Blackstar'),
    ('https://market.yandex.ru/product--akkumuliator-karcher-battery-power-18-25-2-445-034-0-li-ion-18-v-2-5-a-ch/849157225',
     'Аккумулятор KARCHER Battery Power 18/25 (2.445-034.0) Li-Ion 18 В 2.5 А·ч'
     ),
    ('https://market.yandex.ru/product--klaviatura-logitech-k360-chernyi/7694162',
     'Клавиатура Logitech K360')
])
@pytest.mark.hobbygames
def test_parser_hobbygames_parse(url, name):
    data = url_parser.parse(url)

    assert data is not None and data.name == name
