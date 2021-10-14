from url_parser.parser import Parser
from url_parser.exceptions import ParseError
from url_parser.secret import YANDEX_COOKIE_SPRAVKA
import requests
from bs4 import BeautifulSoup


@Parser.register('market.yandex.ru')
class YandexParser(Parser):
    def __repr__(self):
        return 'yandex_parser'

    def fetch(self):
        headers = {
            'User-Agent':
            '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'''
        }
        cookies = {
            'spravka':
            YANDEX_COOKIE_SPRAVKA,
        }
        try:
            result = requests.get(self.url, headers=headers, cookies=cookies)
            result.raise_for_status()
            html = result.text
            return html
        except (requests.RequestException, ValueError) as e:
            raise ParseError(f'{self}/get_html_from_request: {e}')

    def get_price(self, soup: BeautifulSoup):
        try:
            div = soup.find('div', class_='_3NaXx _3kWlK')
            span = div.find('span').find('span')
            price_text = span.text
            price_text = ''.join([s for s in price_text if s.isdigit()])
            price = float(price_text)
            return price
        except (AttributeError, ValueError) as e:
            raise ParseError(f'{self} get_price() {e}')

    def get_name(self, soup: BeautifulSoup) -> str:
        try:
            div = soup.find('h1', class_='_1BWd_ _2OAAC undefined')
            name_text = div.text
            name_text = name_text.replace('\n', '')
            return name_text
        except AttributeError as e:
            raise ParseError(f'{self}/get_name: {e}')

    def get_description(self, soup):
        return ''

    def get_image(self, soup):
        try:
            el = soup.find('img', class_='_3Wp6V')
            picture = el.get('src')
            return picture
        except AttributeError as e:
            raise ParseError(f'{self}/get_picture: {e}')


@Parser.register('hobbygames.ru')
class HobbyGamesParser(Parser):
    def __repr__(self):
        return 'hobbygames parser'

    def get_price(self, soup: BeautifulSoup) -> float:
        try:
            div = soup.find('div', class_='price price-new')
            price_text = div.text
            price_text = ''.join([s for s in price_text if s.isdigit()])
            price = float(price_text)
            return price
        except (AttributeError, ValueError) as e:
            raise ParseError(f'{self} get_price() {e}')

    def get_name(self, soup: BeautifulSoup) -> str:
        try:
            div = soup.find('div', class_='product-info__main')
            name_text = div.text
            name_text = name_text.replace('\n', '')
            return name_text
        except AttributeError as e:
            raise ParseError(f'{self} get_name() {e}')

    def get_description(self, soup: BeautifulSoup) -> str:
        try:
            div = soup.find('div', class_='desc-text')
            desc_text = div.text
            return desc_text
        except AttributeError as e:
            raise ParseError(f'{self} get_description() {e}')

    def get_image(self, soup: BeautifulSoup) -> str:
        try:
            el = soup.find('a', class_='lightGallery')
            picture = el.get('href')
            return picture
        except AttributeError as e:
            raise ParseError(f'{self} get_picture() {e}')
