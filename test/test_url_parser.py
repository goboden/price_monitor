import url_parser
import pytest


@pytest.mark.hobbygames
def test_parser_wrong_domain():
    url = 'https://hobbygames.com/codex-deathwatch-hardback'
    assert pytest.raises(url_parser.exceptions.ParserNotFoundError,
                         url_parser.parse, url)


@pytest.mark.hobbygames
def test_parser_hobbygames_n1():
    url = 'https://hobbygames.ru/codex-deathwatch-hardback'
    data = url_parser.parse(url)

    assert data.price == 2767.0
    assert data.name == 'Codex: Deathwatch 8th edition (Hardback)'
    assert data.description != ''
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


@pytest.mark.yandex
def test_parser_get_info_yandex_one():
    url = 'https://market.yandex.ru/product--akkumuliator-karcher-battery-power-18-25-2-445-034-0-li-ion-18-v-2-5-a-ch/849157225'
    data = url_parser.parse(url)

    assert data.price == 4139.0
    assert data.name == 'Аккумулятор KARCHER Battery Power 18/25 (2.445-034.0) Li-Ion 18 В 2.5 А·ч'
    assert data.description == ''
    assert data.image != ''


@pytest.mark.yandex
def test_parser_get_info_yandex_two():
    url = 'https://market.yandex.ru/product--klaviatura-logitech-k360-chernyi/7694162'
    data = url_parser.parse(url)

    assert data.price == 2390.0
    assert data.name == 'Клавиатура Logitech K360'
    assert data.description == ''
    assert data.image != ''
