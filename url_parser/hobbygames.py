from bs4 import BeautifulSoup
import logging
from url_parser.parser import GenegalParser


logging.basicConfig(filename='hobbygames.log', level=logging.INFO)
logging.info('hobbygames')


def get_price(soup: BeautifulSoup) -> float:
    div = soup.find('div', class_='price price-new')
    price_text = div.text
    price_text = ''.join([s for s in price_text if s.isdigit()])
    try:
        price = float(price_text)
    except ValueError as e:
        logging.info(f'ValueError: {e}')
    return price


def get_name(soup: BeautifulSoup) -> str:
    div = soup.find('div', class_='product-info__main')
    name_text = div.text
    name_text = name_text.replace('\n', '')
    return name_text


def get_description(soup: BeautifulSoup) -> str:
    div = soup.find('div', class_='desc-text')
    desc_text = div.text
    return desc_text


def get_picture(soup: BeautifulSoup) -> str:
    el = soup.find('a', class_='lightGallery')
    picture = el.get('href')
    return picture


class Parser(GenegalParser):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        logging.info(f'New parser {url}')
        logging.info(f'... {self.cache_filename}')

    def get_info(self):
        if self.html:
            soup = BeautifulSoup(self.html, 'html.parser')
            self.info['price'] = get_price(soup)
            self.info['name'] = get_name(soup)
            self.info['description'] = get_description(soup)
            self.info['picture'] = get_picture(soup)
        else:
            logging.info('get_info(): No html')
        return self.info
