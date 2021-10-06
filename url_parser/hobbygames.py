from bs4 import BeautifulSoup
from url_parser.parser import GenegalParser


class Parser(GenegalParser):
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    def get_price(self):
        if self.html:
            soup = BeautifulSoup(self.html, 'html.parser')
            price_div = soup.find('div', class_='price price-new')
            return price_div
        return False
