import requests
from bs4 import BeautifulSoup
from url_parser.parser import GeneralParser, ParseError
import url_parser.secret as secret


class Parser(GeneralParser):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    def __repr__(self):
        return 'yandex parser'

    def get_html_from_request(self, url):
        headers = {
            'User-Agent':
            '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
            (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'''
        }
        cookies = {
            'spravka':
            secret.YANDEX_COOKIE_SPRAVKA,
        }

        try:
            result = requests.get(url, headers=headers, cookies=cookies)
            result.raise_for_status()
            return result.text
        except (requests.RequestException, ValueError):
            return False

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
            div = soup.find('h1', class_='1_1BWd_ _2OAAC undefined')
            name_text = div.text
            name_text = name_text.replace('\n', '')
            return name_text
        except AttributeError as e:
            raise ParseError(f'{self} get_name() {e}')

    def get_description(self, soup):
        return 'Description'

    def get_picture(self, soup):
        return 'Picture'
