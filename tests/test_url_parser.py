import url_parser
from url_parser.exceptions import BadURLError, ParserNotFoundError
from url_parser.exceptions import FetchError, ParseError
import pytest


@pytest.mark.parametrize('url, exception',
                         [('hobbygames.ru', BadURLError),
                          ('https://hobbygames.com', ParserNotFoundError),
                          ('https://hobbygames.ru/corvus-error', FetchError),
                          ('https://hobbygames.ru', ParseError)])
def test_parser_init(url, exception):
    with pytest.raises(exception):
        url_parser.parse(url)


def test_fetch():
    pass
