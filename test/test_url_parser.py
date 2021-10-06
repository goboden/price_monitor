import url_parser
import pytest


def test_parser_wrong_domain():
    url = 'https://hobbygames.com/codex-deathwatch-hardback'
    assert pytest.raises(url_parser.ParserNotFoundError,
                         url_parser.get_parser, url)


def test_parser_get_info():
    url = 'https://hobbygames.ru/codex-deathwatch-hardback'
    parser = url_parser.get_parser(url)
    parser.get_html()
    info = parser.get_info()

    assert info['price'] == 2767.0
    assert info['name'] == 'Codex: Deathwatch 8th edition (Hardback)'
    assert info['description'] != ''
    assert info['picture'] != ''
