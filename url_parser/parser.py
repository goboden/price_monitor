from urllib.parse import urlparse
from pathlib import Path
import os
from datetime import datetime
import requests


def get_file_ttl(filename):
    file_time = os.path.getmtime(filename)
    delta = datetime.now() - datetime.fromtimestamp(file_time)
    return int(round(delta.seconds / 60, 0))


def get_cache_filename(url: str):
    parse_result = urlparse(url)
    filename = f'{parse_result.netloc}{parse_result.path}'
    filename = filename.translate(str.maketrans('./', '__')) + '.html'
    return Path(__file__).parent.joinpath('cache').joinpath(filename)


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


class GenegalParser():
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

    def get_html(self):
        if self.from_cache:
            self.html = get_html_from_cache(self.url, ttl=self.cache_ttl)
        if not self.html:
            try:
                result = requests.get(self.url)
                result.raise_for_status()
                self.html = result.text
                if self.html:
                    save_html_to_cache(self.html, self.url)
            except (requests.RequestException, ValueError):
                pass

    def try_to_get(self):
        self.get_html()
        if self.html:
            return True
        return False

    def get_info(self):
        raise NotImplementedError
