from url_parser import cache
from url_parser.exceptions import NotExistCacheError, TooOldCacheError
import pytest


@pytest.fixture(scope='function')
def url(request):
    url = 'https://hobbygames.ru/stormfang-gunship-2014'
    html_cache = cache.HTMLCache(url)
    html_cache.write('HTML')

    def delete_cache_file():
        html_cache.delete()

    request.addfinalizer(delete_cache_file)

    return url


def test_cache(url):
    html_cache = cache.HTMLCache(url)
    assert html_cache.read() == 'HTML'


def test_cache_too_old(url):
    html_cache = cache.HTMLCache(url)
    html_cache.ttl = 0
    with pytest.raises(TooOldCacheError):
        html_cache.read()


def test_cache_no_file():
    url = 'https://hobbygames.ru/stormfang-gunship-3000'
    html_cache = cache.HTMLCache(url)
    with pytest.raises(NotExistCacheError):
        html_cache.read()
