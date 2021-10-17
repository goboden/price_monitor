from abc import ABC, abstractmethod
from dataclasses import dataclass
import validators
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from url_parser.cache import HTMLCache
from url_parser.exceptions import BadURLError
from url_parser.exceptions import ParserNotFoundError, ParseError, FetchError
from url_parser.exceptions import NotExistCacheError, TooOldCacheError


@dataclass
class ParsedData:
    name: str
    description: str
    image: str
    price: float

    def __init__(self):
        pass


class Parser(ABC):
    _REGISTRY = {}

    @classmethod
    def create(cls, url) -> 'Parser':
        if not validators.url(url):
            raise BadURLError(url)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        klass = cls._REGISTRY.get(domain)
        if not klass:
            raise ParserNotFoundError(domain)
        return klass(url)

    @classmethod
    def register(cls, domain):
        def decorator(klass):
            cls._REGISTRY[domain] = klass
            return klass
        return decorator

    @abstractmethod
    def get_price(self, soup):
        pass

    @abstractmethod
    def get_name(self, soup):
        pass

    @abstractmethod
    def get_description(self, soup):
        pass

    @abstractmethod
    def get_image(self, soup):
        pass

    def __init__(self, url):
        self.url = url
        self._html = None
        self.use_cache = True
        self.cache = HTMLCache(url)
        self.data = None

    def fetch(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            html = result.text
            return html
        except (requests.RequestException, ValueError):
            raise FetchError

    def parse(self):
        if self.use_cache:
            try:
                self._html = self.cache.read()
            except (NotExistCacheError, TooOldCacheError):
                self._html = self.fetch()
                self.cache.write(self._html)
        else:
            self._html = self.fetch()

        if self._html:
            try:
                data = ParsedData()
                soup = BeautifulSoup(self._html, 'html.parser')
                data.price = self.get_price(soup)
                data.name = self.get_name(soup)
                data.description = self.get_description(soup)
                data.image = self.get_image(soup)
                self.data = data
            except ParseError as e:
                # log
                self.cache.delete()
                raise e
        else:
            # log
            raise FetchError
