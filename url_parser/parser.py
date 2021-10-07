from urllib.parse import urlparse
from pathlib import Path
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import logging


logging.basicConfig(filename='parser.log', level=logging.INFO)


class ParseError(Exception):
    def __init__(self, info):
        self.message = f'Parse error: {info}'
        super().__init__(self.message)


def get_chache_dir():
    pafent_dir = Path(__file__).parent
    cache_dir = pafent_dir.joinpath('cache')
    if not cache_dir.exists():
        os.mkdir(cache_dir)
    return cache_dir


def get_file_ttl(filename):
    file_time = os.path.getmtime(filename)
    delta = datetime.now() - datetime.fromtimestamp(file_time)
    return int(round(delta.seconds / 60, 0))


def get_cache_filename(url: str):
    cache_dir = get_chache_dir()
    parse_result = urlparse(url)
    filename = f'{parse_result.netloc}{parse_result.path}'
    filename = filename.translate(str.maketrans('./', '__')) + '.html'
    return cache_dir.joinpath(filename)


def get_html_from_cache(url: str, ttl: int) -> str:
    html = ''
    cache_filename = get_cache_filename(url)
    if cache_filename.exists():
        file_ttl = get_file_ttl(cache_filename)
        if file_ttl < ttl:
            with open(cache_filename, 'r', encoding='utf-8') as f:
                html = f.read()
    return html


def save_html_to_cache(html: str, url):
    if html:
        cache_filename = get_cache_filename(url)
        with open(cache_filename, 'w', encoding='utf-8') as f:
            f.write(html)


class GeneralParser():
    @classmethod
    def get_html_from_request(cls, url):
        try:
            result = requests.get(url)
            result.raise_for_status()
            html = result.text
            return html
        except (requests.RequestException, ValueError) as e:
            logging.info(e)

    @classmethod
    def get_price(cls, soup):
        raise ParseError('get_price() is not implemented')

    @classmethod
    def get_name(cls, soup):
        raise ParseError('get_name() is not implemented')

    @classmethod
    def get_description(cls, soup):
        raise ParseError('get_description() is not implemented')

    @classmethod
    def get_picture(cls, soup):
        raise ParseError('get_picture() is not implemented')

    def __init__(self, url, from_cache=True, cache_ttl=1440):
        self.url = url
        self.from_cache = from_cache
        self.cache_ttl = cache_ttl
        self.cache_filename = get_cache_filename(self.url)
        self.html = ''
        self.info = {
            'name': '',
            'description': '',
            'picture': '',
            'price': 0
        }

    def __repr__(self):
        return 'general_parser'

    def get_html(self):
        if self.from_cache:
            self.html = get_html_from_cache(self.url, ttl=self.cache_ttl)
        if not self.html:
            try:
                self.html = self.get_html_from_request(self.url)
                if self.html:
                    save_html_to_cache(self.html, self.url)
            except Exception as e:
                logging.info(e)

    def get_info(self):
        if self.html:
            info = self.info.copy()
            try:
                soup = BeautifulSoup(self.html, 'html.parser')
                self.info['price'] = self.get_price(soup)
                self.info['name'] = self.get_name(soup)
                self.info['description'] = self.get_description(soup)
                self.info['picture'] = self.get_picture(soup)
            except ParseError as e:
                self.info = info
                logging.info(e)
        else:
            logging.info('Parse error: No html')
        return self.info
