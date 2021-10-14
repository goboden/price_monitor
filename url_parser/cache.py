from pathlib import Path
import os
from urllib.parse import urlparse
from datetime import datetime


def default_dir():
    pafent_dir = Path(__file__).parent
    cache_dir = pafent_dir.joinpath('cache')
    if not cache_dir.exists():
        os.mkdir(cache_dir)
    return cache_dir


class HTMLCache():
    def __init__(self):
        self.ttl = 1440
        self.dir = default_dir()
        self._url = None
        self._filename = None
        self._file_ttl = None

    def from_url(self, url):
        self._url = url
        self._set_filename()

    def _set_filename(self):
        parse_result = urlparse(self._url)
        filename = f'{parse_result.netloc}{parse_result.path}'
        filename = filename.translate(str.maketrans('./', '__')) + '.html'
        self._filename = self.dir.joinpath(filename)

    def _set_ttl(self):
        file_time = os.path.getmtime(self._filename)
        delta = datetime.now() - datetime.fromtimestamp(file_time)
        self._file_ttl = int(round(delta.seconds / 60, 0))

    def read(self):
        html = None
        
        if self._filename.exists():
            self._set_ttl()
            if self._file_ttl < self.ttl:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    html = f.read()
            else:
                raise Exception('---2---')
        else:
            raise Exception('---1---')
        return html

    def write(self, html):
        with open(self._filename, 'w', encoding='utf-8') as f:
            f.write(html)
