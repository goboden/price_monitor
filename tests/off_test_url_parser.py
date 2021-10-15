import url_parser
import pytest


@pytest.mark.hobbygames
def test_parser_wrong_domain():
    url = 'https://hobbygames.com/codex-deathwatch-hardback'
    with pytest.raises(url_parser.exceptions.ParserNotFoundError):
        data = url_parser.parse(url)


@pytest.mark.parametrize(
    'url, price, name',
    [('https://hobbygames.ru/codex-deathwatch-hardback',
      2767.0,
      'Codex: Deathwatch 8th edition (Hardback)'),
     ('https://hobbygames.ru/corvus-blackstar',
      4883.0,
      'Corvus Blackstar')])
@pytest.mark.hobbygames
def test_parser_hobbygames_parse(url, price, name):
    data = url_parser.parse(url)

    assert data.price == price
    assert data.name == name
    assert data.description != ''
    assert data.image != ''


@pytest.mark.parametrize(
    'url, price, name',
    [('https://market.yandex.ru/product--akkumuliator-karcher-battery-power-18-25-2-445-034-0-li-ion-18-v-2-5-a-ch/849157225', 4139.0,
      'Аккумулятор KARCHER Battery Power 18/25 (2.445-034.0) Li-Ion 18 В 2.5 А·ч'),
     ('https://market.yandex.ru/product--klaviatura-logitech-k360-chernyi/7694162', 2263.0, 'Клавиатура Logitech K360')])
@pytest.mark.yandex
def test_parser_get_info_yandex(url, price, name):
    data = url_parser.parse(url)

    assert data is not None
    assert data.price == price
    assert data.name == name
    assert data.description == ''
    assert data.image != ''


@pytest.mark.hobbygames
def test_parser_get_info_no_cache():
    url = 'https://hobbygames.ru/corvus-blackstar'
    # data = url_parser.parse(url, no_cache=True)
    data = url_parser.parse(url, cache_ttl=0)

    assert data.price == 4883.0
    assert data.name == 'Corvus Blackstar'
    assert data.description != ''
    assert data.image != ''
