from bs4 import BeautifulSoup
from url_parser.parser import GeneralParser, ParseError


class Parser(GeneralParser):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    def __repr__(self):
        return 'hobbygames parser'

    def get_price(self, soup: BeautifulSoup) -> float:
        try:
            div = soup.find('div', class_='price')
            if not div:
                div = soup.find('div', class_='price price-new') # ???
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

    def get_picture(self, soup: BeautifulSoup) -> str:
        try:
            el = soup.find('a', class_='lightGallery')
            picture = el.get('href')
            return picture
        except AttributeError as e:
            raise ParseError(f'{self} get_picture() {e}')
