import url_parser
import pytest


@pytest.mark.hobbygames
def test_parser_wrong_domain():
    url = 'https://hobbygames.com/codex-deathwatch-hardback'
    assert pytest.raises(url_parser.ParserNotFoundError,
                         url_parser.get_parser, url)


@pytest.mark.hobbygames
def test_parser_get_info():
    url = 'https://hobbygames.ru/codex-deathwatch-hardback'
    parser = url_parser.get_parser(url)
    parser.get_html()
    info = parser.get_info()

    assert info['price'] == 2767.0
    assert info['name'] == 'Codex: Deathwatch 8th edition (Hardback)'
    assert info['description'] != ''
    assert info['picture'] != ''


@pytest.mark.hobbygames
def test_parser_get_info_no_cache():
    url = 'https://hobbygames.ru/corvus-blackstar'
    parser = url_parser.get_parser(url, cache_ttl=0)
    parser.get_html()
    info = parser.get_info()

    assert info['price'] == 4883.0
    assert info['name'] == 'Corvus Blackstar'
    assert info['description'] != ''
    assert info['picture'] != ''


@pytest.mark.yandex
def test_parser_get_info_yandex_one():
    url = 'https://market.yandex.ru/product--akkumuliator-karcher-battery-power-18-25-2-445-034-0-li-ion-18-v-2-5-a-ch/849157225'
    parser = url_parser.get_parser(url)
    parser.get_html()
    info = parser.get_info()

    assert info['price'] == 4580.0
    assert info[
        'name'] == 'Аккумулятор KARCHER Battery Power 18/25 (2.445-034.0) Li-Ion 18 В 2.5 А·ч'
    assert info['description'] != ''
    assert info['picture'] != ''


@pytest.mark.yandex
def test_parser_get_info_yandex_two():
    url = 'https://market.yandex.ru/product--klaviatura-logitech-k360-chernyi/7694162'
    parser = url_parser.get_parser(url)
    parser.get_html()
    info = parser.get_info()

    assert info['price'] == 2313.0
    assert info['name'] == 'Клавиатура Logitech K360'
    assert info['description'] != ''
    assert info['picture'] != ''
